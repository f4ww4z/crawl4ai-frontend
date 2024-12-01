# crawl4ai-frontend

A FastAPI-based frontend for crawl4ai that provides a web interface and REST API for crawling websites and converting them to markdown format.

## Features

- Web interface for easy interaction
- REST API for programmatic access
- Recursive website crawling with configurable depth
- Automatic conversion of web pages to markdown format
- Background job processing with status tracking
- Results downloadable as ZIP archives
- Docker support for easy deployment

## Installation

### Local Installation

1. Ensure you have Python 3.10+ and Poetry installed
2. Clone the repository
3. Install dependencies:
```bash
poetry install
```

### Docker Installation

1. Ensure you have Docker installed
2. Build the image:
```bash
docker build -t crawl4ai-frontend .
```

Or use docker-compose:
```bash
docker-compose up -d
```

## Usage

### Running Locally

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

### Running with Docker

```bash
docker run -p 8000:8000 crawl4ai-frontend
```

Then open http://localhost:8000 in your browser.

## API Documentation

### Start a Crawl Job

```http
POST /api/crawl
```

Request body:
```json
{
    "url": "https://example.com",
    "limit": 10
}
```

Response:
```json
{
    "job_id": "uuid",
    "status": "starting",
    "progress": 0
}
```

### Check Job Status

```http
GET /api/status/{job_id}
```

Response:
```json
{
    "job_id": "uuid",
    "status": "processing|completed|failed",
    "progress": 5,
    "total_pages": 10,
    "current_url": "https://example.com/page"
}
```

### Download Results

```http
GET /api/download/{job_id}
```

Returns a ZIP file containing the crawled pages in markdown format.

## Dependencies

- Python 3.10+
- FastAPI
- Crawl4AI
- aiofiles
- Poetry (for dependency management)

## Development

For development, additional dependencies can be installed:
```bash
poetry install --with dev
```

Development dependencies include:
- autopep8 (code formatting)
- djlint (HTML template linting)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
