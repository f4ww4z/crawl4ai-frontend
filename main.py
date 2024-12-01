import asyncio
import os
import shutil
import re
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict
from crawl4ai import AsyncWebCrawler
import uuid
import aiofiles
from urllib.parse import urlparse, unquote

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store crawl jobs status
crawl_jobs: Dict[str, dict] = {}

class CrawlRequest(BaseModel):
    url: str
    limit: int = 10

class CrawlResponse(BaseModel):
    job_id: str
    status: str
    progress: int = 0
    total_pages: int = 0
    current_url: Optional[str] = None

def clean_path(url: str, base_url: str) -> str:
    """Extract and clean the path from URL relative to base URL"""
    # URL decode both URLs to handle any encoded characters
    url = unquote(url)
    base_url = unquote(base_url)
    
    # Remove base URL to get the relative path
    path = url.replace(base_url, '')
    
    # If path starts with /, remove it
    path = path.lstrip('/')
    
    # Handle fragment identifiers (#)
    if '#' in path:
        path = path.split('#')[1]  # Take the fragment part
    else:
        # Remove query parameters if no fragment
        path = path.split('?')[0]
    
    # If path is empty after cleaning, return empty string
    if not path:
        return ''
    
    # Clean special characters and convert spaces
    clean = re.sub(r'[^\w\s-]', '', path)
    clean = re.sub(r'\s+', '_', clean.strip())
    return clean.lower()

async def process_url(url: str, output_dir: str, crawler: AsyncWebCrawler, job_id: str):
    """Process a single URL and save markdown"""
    try:
        result = await crawler.arun(
            url=url,
            remove_overlay_elements=True,
            bypass_cache=True
        )
        
        if result.success:
            # Get title from metadata
            metadata = result.metadata
            title = metadata['title']
            # Clean title for filename
            clean_title = re.sub(r'[^\w\s-]', '', title)
            clean_title = re.sub(r'\s+', '_', clean_title.strip())
            
            # Get and clean URL path
            path_suffix = clean_path(url, crawl_jobs[job_id]["base_url"])
            
            # Combine title and path for unique filename
            filename = f"{clean_title.lower()}"
            if path_suffix:
                filename += f"_{path_suffix}"
            filename += ".md"
            
            # Save markdown
            filepath = os.path.join(output_dir, filename)
            async with aiofiles.open(filepath, 'w') as f:
                await f.write(result.markdown)
            
            # Return internal links
            return result.links.get("internal", [])
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
    return []

async def crawl_website(job_id: str, url: str, limit: int):
    """Recursively crawl website and update job status"""
    try:
        # Create output directory
        output_dir = f"output/output_{job_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Store the base URL for this job
        crawl_jobs[job_id]["base_url"] = url
        
        # Initialize crawler
        async with AsyncWebCrawler(verbose=True) as crawler:
            processed_urls = set()
            urls_to_process = {url}
            
            while urls_to_process and len(processed_urls) < limit:
                current_url = urls_to_process.pop()
                
                if current_url in processed_urls:
                    continue
                
                # Update job status
                crawl_jobs[job_id].update({
                    "status": "processing",
                    "progress": len(processed_urls),
                    "current_url": current_url
                })
                
                # Process URL and get internal links
                internal_links = await process_url(current_url, output_dir, crawler, job_id)
                processed_urls.add(current_url)
                
                # Add new internal links that contain the base URL
                for link in internal_links:
                    if isinstance(link, dict):
                        link_url = link.get("href", "")
                    else:
                        link_url = link
                        
                    if link_url and link_url.startswith(url) and link_url not in processed_urls:
                        urls_to_process.add(link_url)
        
        # Create zip file
        shutil.make_archive(output_dir, 'zip', output_dir)
        
        # Update final status
        crawl_jobs[job_id].update({
            "status": "completed",
            "progress": len(processed_urls),
            "total_pages": len(processed_urls)
        })
        
        # Cleanup output directory
        shutil.rmtree(output_dir)
        
    except Exception as e:
        crawl_jobs[job_id]["status"] = "failed"
        print(f"Crawl failed: {str(e)}")

@app.post("/api/crawl", response_model=CrawlResponse)
async def start_crawl(request: CrawlRequest):
    job_id = str(uuid.uuid4())
    crawl_jobs[job_id] = {
        "status": "starting",
        "progress": 0,
        "total_pages": 0,
        "base_url": request.url  # Store the base URL
    }
    
    # Start crawl in background
    asyncio.create_task(crawl_website(job_id, request.url, request.limit))
    
    return CrawlResponse(
        job_id=job_id,
        status="starting",
        progress=0
    )

@app.get("/api/status/{job_id}", response_model=CrawlResponse)
async def get_status(job_id: str):
    if job_id not in crawl_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = crawl_jobs[job_id]
    return CrawlResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        total_pages=job["total_pages"],
        current_url=job.get("current_url")
    )

@app.get("/api/download/{job_id}")
async def download_results(job_id: str):
    if job_id not in crawl_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = crawl_jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    
    zip_path = f"output/output_{job_id}.zip"
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Results not found")
    
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="crawl_results.zip"
    )

# Serve index.html
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
