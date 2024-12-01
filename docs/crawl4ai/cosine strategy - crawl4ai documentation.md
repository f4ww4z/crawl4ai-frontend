# Cosine Strategy

The Cosine Strategy in Crawl4AI uses similarity-based clustering to identify and extract relevant content sections from web pages. This strategy is particularly useful when you need to find and extract content based on semantic similarity rather than structural patterns.

## How It Works

The Cosine Strategy:
1\. Breaks down page content into meaningful chunks
2\. Converts text into vector representations
3\. Calculates similarity between chunks
4\. Clusters similar content together
5\. Ranks and filters content based on relevance

## Basic Usage

```hljs csharp
from crawl4ai.extraction_strategy import CosineStrategy

strategy = CosineStrategy(
    semantic_filter="product reviews",    # Target content type
    word_count_threshold=10,             # Minimum words per cluster
    sim_threshold=0.3                    # Similarity threshold
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com/reviews",
        extraction_strategy=strategy
    )

    content = result.extracted_content

```

## Configuration Options

### Core Parameters

```hljs python
CosineStrategy(
    # Content Filtering
    semantic_filter: str = None,       # Keywords/topic for content filtering
    word_count_threshold: int = 10,    # Minimum words per cluster
    sim_threshold: float = 0.3,        # Similarity threshold (0.0 to 1.0)

    # Clustering Parameters
    max_dist: float = 0.2,            # Maximum distance for clustering
    linkage_method: str = 'ward',      # Clustering linkage method
    top_k: int = 3,                   # Number of top categories to extract

    # Model Configuration
    model_name: str = 'sentence-transformers/all-MiniLM-L6-v2',  # Embedding model

    verbose: bool = False             # Enable logging
)

```

### Parameter Details

01. **semantic\_filter**
02. Sets the target topic or content type
03. Use keywords relevant to your desired content
04. Example: "technical specifications", "user reviews", "pricing information"

05. **sim\_threshold**

06. Controls how similar content must be to be grouped together
07. Higher values (e.g., 0.8) mean stricter matching
08. Lower values (e.g., 0.3) allow more variation




    ```hljs ini
    # Strict matching
    strategy = CosineStrategy(sim_threshold=0.8)

    # Loose matching
    strategy = CosineStrategy(sim_threshold=0.3)

    ```

09. **word\_count\_threshold**

10. Filters out short content blocks
11. Helps eliminate noise and irrelevant content




    ```hljs ini
    # Only consider substantial paragraphs
    strategy = CosineStrategy(word_count_threshold=50)

    ```

12. **top\_k**

13. Number of top content clusters to return
14. Higher values return more diverse content



    ```hljs ini
    # Get top 5 most relevant content clusters
    strategy = CosineStrategy(top_k=5)

    ```


## Use Cases

### 1\. Article Content Extraction

```hljs makefile
strategy = CosineStrategy(
    semantic_filter="main article content",
    word_count_threshold=100,  # Longer blocks for articles
    top_k=1                   # Usually want single main content
)

result = await crawler.arun(
    url="https://example.com/blog/post",
    extraction_strategy=strategy
)

```

### 2\. Product Review Analysis

```hljs makefile
strategy = CosineStrategy(
    semantic_filter="customer reviews and ratings",
    word_count_threshold=20,   # Reviews can be shorter
    top_k=10,                 # Get multiple reviews
    sim_threshold=0.4         # Allow variety in review content
)

```

### 3\. Technical Documentation

```hljs makefile
strategy = CosineStrategy(
    semantic_filter="technical specifications documentation",
    word_count_threshold=30,
    sim_threshold=0.6,        # Stricter matching for technical content
    max_dist=0.3             # Allow related technical sections
)

```

## Advanced Features

### Custom Clustering

```hljs bash
strategy = CosineStrategy(
    linkage_method='complete',  # Alternative clustering method
    max_dist=0.4,              # Larger clusters
    model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'  # Multilingual support
)

```

### Content Filtering Pipeline

```hljs python
strategy = CosineStrategy(
    semantic_filter="pricing plans features",
    word_count_threshold=15,
    sim_threshold=0.5,
    top_k=3
)

async def extract_pricing_features(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            extraction_strategy=strategy
        )

        if result.success:
            content = json.loads(result.extracted_content)
            return {
                'pricing_features': content,
                'clusters': len(content),
                'similarity_scores': [item['score'] for item in content]
            }

```

## Best Practices

01. **Adjust Thresholds Iteratively**
02. Start with default values
03. Adjust based on results
04. Monitor clustering quality

05. **Choose Appropriate Word Count Thresholds**

06. Higher for articles (100+)
07. Lower for reviews/comments (20+)
08. Medium for product descriptions (50+)

09. **Optimize Performance**



    ```hljs graphql
    strategy = CosineStrategy(
        word_count_threshold=10,  # Filter early
        top_k=5,                 # Limit results
        verbose=True             # Monitor performance
    )

    ```

10. **Handle Different Content Types**



    ```hljs makefile
    # For mixed content pages
    strategy = CosineStrategy(
        semantic_filter="product features",
        sim_threshold=0.4,      # More flexible matching
        max_dist=0.3,          # Larger clusters
        top_k=3                # Multiple relevant sections
    )

    ```


## Error Handling

```hljs python
try:
    result = await crawler.arun(
        url="https://example.com",
        extraction_strategy=strategy
    )

    if result.success:
        content = json.loads(result.extracted_content)
        if not content:
            print("No relevant content found")
    else:
        print(f"Extraction failed: {result.error_message}")

except Exception as e:
    print(f"Error during extraction: {str(e)}")

```

The Cosine Strategy is particularly effective when:
\- Content structure is inconsistent
\- You need semantic understanding
\- You want to find similar content blocks
\- Structure-based extraction (CSS/XPath) isn't reliable

It works well with other strategies and can be used as a pre-processing step for LLM-based extraction.

* * *