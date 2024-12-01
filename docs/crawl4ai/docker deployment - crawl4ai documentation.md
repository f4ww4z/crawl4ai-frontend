# Docker Deployment

Crawl4AI provides official Docker images for easy deployment and scalability. This guide covers installation, configuration, and usage of Crawl4AI in Docker environments.

## Quick Start 🚀

Pull and run the basic version:

```hljs bash
docker pull unclecode/crawl4ai:basic
docker run -p 11235:11235 unclecode/crawl4ai:basic

```

Test the deployment:

```hljs makefile
import requests

# Test health endpoint
health = requests.get("http://localhost:11235/health")
print("Health check:", health.json())

# Test basic crawl
response = requests.post(
    "http://localhost:11235/crawl",
    json={
        "urls": "https://www.nbcnews.com/business",
        "priority": 10
    }
)
task_id = response.json()["task_id"]
print("Task ID:", task_id)

```

## Available Images 🏷️

- `unclecode/crawl4ai:basic` \- Basic web crawling capabilities
- `unclecode/crawl4ai:all` \- Full installation with all features
- `unclecode/crawl4ai:gpu` \- GPU-enabled version for ML features

## Configuration Options 🔧

### Environment Variables

```hljs bash
docker run -p 11235:11235 \
    -e MAX_CONCURRENT_TASKS=5 \
    -e OPENAI_API_KEY=your_key \
    unclecode/crawl4ai:all

```

### Volume Mounting

Mount a directory for persistent data:

```hljs bash
docker run -p 11235:11235 \
    -v $(pwd)/data:/app/data \
    unclecode/crawl4ai:all

```

### Resource Limits

Control container resources:

```hljs sql
docker run -p 11235:11235 \
    --memory=4g \
    --cpus=2 \
    unclecode/crawl4ai:all

```

## Usage Examples 📝

### Basic Crawling

```hljs makefile
request = {
    "urls": "https://www.nbcnews.com/business",
    "priority": 10
}

response = requests.post("http://localhost:11235/crawl", json=request)
task_id = response.json()["task_id"]

# Get results
result = requests.get(f"http://localhost:11235/task/{task_id}")

```

### Structured Data Extraction

```hljs graphql
schema = {
    "name": "Crypto Prices",
    "baseSelector": ".cds-tableRow-t45thuk",
    "fields": [\
        {\
            "name": "crypto",\
            "selector": "td:nth-child(1) h2",\
            "type": "text",\
        },\
        {\
            "name": "price",\
            "selector": "td:nth-child(2)",\
            "type": "text",\
        }\
    ],
}

request = {
    "urls": "https://www.coinbase.com/explore",
    "extraction_config": {
        "type": "json_css",
        "params": {"schema": schema}
    }
}

```

### Dynamic Content Handling

```hljs makefile
request = {
    "urls": "https://www.nbcnews.com/business",
    "js_code": [\
        "const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More')); loadMoreButton && loadMoreButton.click();"\
    ],
    "wait_for": "article.tease-card:nth-child(10)"
}

```

### AI-Powered Extraction (Full Version)

```hljs makefile
request = {
    "urls": "https://www.nbcnews.com/business",
    "extraction_config": {
        "type": "cosine",
        "params": {
            "semantic_filter": "business finance economy",
            "word_count_threshold": 10,
            "max_dist": 0.2,
            "top_k": 3
        }
    }
}

```

## Platform-Specific Instructions 💻

### macOS

```hljs bash
docker pull unclecode/crawl4ai:basic
docker run -p 11235:11235 unclecode/crawl4ai:basic

```

### Ubuntu

```hljs bash
# Basic version
docker pull unclecode/crawl4ai:basic
docker run -p 11235:11235 unclecode/crawl4ai:basic

# With GPU support
docker pull unclecode/crawl4ai:gpu
docker run --gpus all -p 11235:11235 unclecode/crawl4ai:gpu

```

### Windows (PowerShell)

```hljs bash
docker pull unclecode/crawl4ai:basic
docker run -p 11235:11235 unclecode/crawl4ai:basic

```

## Testing 🧪

Save this as `test_docker.py`:

```hljs python
import requests
import json
import time
import sys

class Crawl4AiTester:
    def __init__(self, base_url: str = "http://localhost:11235"):
        self.base_url = base_url

    def submit_and_wait(self, request_data: dict, timeout: int = 300) -> dict:
        # Submit crawl job
        response = requests.post(f"{self.base_url}/crawl", json=request_data)
        task_id = response.json()["task_id"]
        print(f"Task ID: {task_id}")

        # Poll for result
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Task {task_id} timeout")

            result = requests.get(f"{self.base_url}/task/{task_id}")
            status = result.json()

            if status["status"] == "completed":
                return status

            time.sleep(2)

def test_deployment():
    tester = Crawl4AiTester()

    # Test basic crawl
    request = {
        "urls": "https://www.nbcnews.com/business",
        "priority": 10
    }

    result = tester.submit_and_wait(request)
    print("Basic crawl successful!")
    print(f"Content length: {len(result['result']['markdown'])}")

if __name__ == "__main__":
    test_deployment()

```

## Advanced Configuration ⚙️

### Crawler Parameters

The `crawler_params` field allows you to configure the browser instance and crawling behavior. Here are key parameters you can use:

```hljs graphql
request = {
    "urls": "https://example.com",
    "crawler_params": {
        # Browser Configuration
        "headless": True,                    # Run in headless mode
        "browser_type": "chromium",          # chromium/firefox/webkit
        "user_agent": "custom-agent",        # Custom user agent
        "proxy": "http://proxy:8080",        # Proxy configuration

        # Performance & Behavior
        "page_timeout": 30000,               # Page load timeout (ms)
        "verbose": True,                     # Enable detailed logging
        "semaphore_count": 5,               # Concurrent request limit

        # Anti-Detection Features
        "simulate_user": True,               # Simulate human behavior
        "magic": True,                       # Advanced anti-detection
        "override_navigator": True,          # Override navigator properties

        # Session Management
        "user_data_dir": "./browser-data",   # Browser profile location
        "use_managed_browser": True,         # Use persistent browser
    }
}

```

### Extra Parameters

The `extra` field allows passing additional parameters directly to the crawler's `arun` function:

```hljs graphql
request = {
    "urls": "https://example.com",
    "extra": {
        "word_count_threshold": 10,          # Min words per block
        "only_text": True,                   # Extract only text
        "bypass_cache": True,                # Force fresh crawl
        "process_iframes": True,             # Include iframe content
    }
}

```

### Complete Examples

1. **Advanced News Crawling**



```hljs graphql
request = {
       "urls": "https://www.nbcnews.com/business",
       "crawler_params": {
           "headless": True,
           "page_timeout": 30000,
           "remove_overlay_elements": True      # Remove popups
       },
       "extra": {
           "word_count_threshold": 50,          # Longer content blocks
           "bypass_cache": True                 # Fresh content
       },
       "css_selector": ".article-body"
}

```

2. **Anti-Detection Configuration**



```hljs graphql
request = {
       "urls": "https://example.com",
       "crawler_params": {
           "simulate_user": True,
           "magic": True,
           "override_navigator": True,
           "user_agent": "Mozilla/5.0 ...",
           "headers": {
               "Accept-Language": "en-US,en;q=0.9"
           }
       }
}

```

3. **LLM Extraction with Custom Parameters**



```hljs graphql
request = {
       "urls": "https://openai.com/pricing",
       "extraction_config": {
           "type": "llm",
           "params": {
               "provider": "openai/gpt-4",
               "schema": pricing_schema
           }
       },
       "crawler_params": {
           "verbose": True,
           "page_timeout": 60000
       },
       "extra": {
           "word_count_threshold": 1,
           "only_text": True
       }
}

```

4. **Session-Based Dynamic Content**



```hljs graphql
request = {
       "urls": "https://example.com",
       "crawler_params": {
           "session_id": "dynamic_session",
           "headless": False,
           "page_timeout": 60000
       },
       "js_code": ["window.scrollTo(0, document.body.scrollHeight);"],
       "wait_for": "js:() => document.querySelectorAll('.item').length > 10",
       "extra": {
           "delay_before_return_html": 2.0
       }
}

```

5. **Screenshot with Custom Timing**



```hljs graphql
request = {
       "urls": "https://example.com",
       "screenshot": True,
       "crawler_params": {
           "headless": True,
           "screenshot_wait_for": ".main-content"
       },
       "extra": {
           "delay_before_return_html": 3.0
       }
}

```


### Parameter Reference Table

| Category | Parameter | Type | Description |
| --- | --- | --- | --- |
| Browser | headless | bool | Run browser in headless mode |
| Browser | browser\_type | str | Browser engine selection |
| Browser | user\_agent | str | Custom user agent string |
| Network | proxy | str | Proxy server URL |
| Network | headers | dict | Custom HTTP headers |
| Timing | page\_timeout | int | Page load timeout (ms) |
| Timing | delay\_before\_return\_html | float | Wait before capture |
| Anti-Detection | simulate\_user | bool | Human behavior simulation |
| Anti-Detection | magic | bool | Advanced protection |
| Session | session\_id | str | Browser session ID |
| Session | user\_data\_dir | str | Profile directory |
| Content | word\_count\_threshold | int | Minimum words per block |
| Content | only\_text | bool | Text-only extraction |
| Content | process\_iframes | bool | Include iframe content |
| Debug | verbose | bool | Detailed logging |
| Debug | log\_console | bool | Browser console logs |

## Troubleshooting 🔍

### Common Issues

1. **Connection Refused**



```hljs javascript
Error: Connection refused at localhost:11235

```



    Solution: Ensure the container is running and ports are properly mapped.

2. **Resource Limits**



```hljs yaml
Error: No available slots

```



    Solution: Increase MAX\_CONCURRENT\_TASKS or container resources.

3. **GPU Access**



```hljs javascript
Error: GPU not found

```



    Solution: Ensure proper NVIDIA drivers and use `--gpus all` flag.


### Debug Mode

Access container for debugging:

```hljs bash
docker run -it --entrypoint /bin/bash unclecode/crawl4ai:all

```

View container logs:

```hljs css
docker logs [container_id]

```

## Best Practices 🌟

01. **Resource Management**
02. Set appropriate memory and CPU limits
03. Monitor resource usage via health endpoint
04. Use basic version for simple crawling tasks

05. **Scaling**

06. Use multiple containers for high load
07. Implement proper load balancing
08. Monitor performance metrics

09. **Security**

10. Use environment variables for sensitive data
11. Implement proper network isolation
12. Regular security updates

## API Reference 📚

### Health Check

```hljs bash
GET /health

```

### Submit Crawl Task

```hljs bash
POST /crawl
Content-Type: application/json

{
    "urls": "string or array",
    "extraction_config": {
        "type": "basic|llm|cosine|json_css",
        "params": {}
    },
    "priority": 1-10,
    "ttl": 3600
}

```

### Get Task Status

```hljs bash
GET /task/{task_id}

```

For more details, visit the [official documentation](https://crawl4ai.com/mkdocs/).

* * *