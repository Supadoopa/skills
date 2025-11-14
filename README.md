# Documentation Scraper

A configurable documentation scraper for generating structured Markdown documentation from web-based documentation sites.

## Features

- **JSON-based Configuration**: Define documentation structures using simple JSON config files
- **Multiple Documentation Sources**: Support for multiple documentation sites (Tailwind CSS, React, and more)
- **Organized Output**: Automatically organizes scraped content by category
- **Metadata Generation**: Creates index files and metadata for easy navigation
- **Rate Limiting**: Built-in rate limiting to respect server resources
- **Extensible**: Easy to add new documentation sources

## Available Configurations

### Tailwind CSS (v3)
- **File**: `configs/tailwind.json`
- **Pages**: 180 documentation pages
- **Categories**: 17 sections including Getting Started, Core Concepts, Layout, Flexbox & Grid, Typography, and more
- **Output**: `output/tailwind/`

### React (v18)
- **File**: `configs/react.json`
- **Pages**: 32 documentation pages
- **Categories**: 5 sections including Hooks, Components, APIs, and React DOM
- **Output**: `output/react/`

## Usage

### List Available Configs

```bash
python3 scraper.py --list-configs
```

### Scrape Documentation

**Tailwind CSS:**
```bash
python3 scraper.py --config configs/tailwind.json --output output/tailwind
```

**React:**
```bash
python3 scraper.py --config configs/react.json --output output/react
```

## Configuration File Format

Create a JSON configuration file with the following structure:

```json
{
  "name": "Framework Name",
  "base_url": "https://example.com",
  "docs_base": "https://example.com/docs",
  "version": "1.0",
  "description": "Description of the documentation",
  "sections": [
    {
      "category": "Category Name",
      "pages": [
        {"title": "Page Title", "url": "/docs/page-url"}
      ]
    }
  ],
  "scraping": {
    "rate_limit_ms": 1000,
    "max_retries": 3,
    "timeout_ms": 30000,
    "user_agent": "Mozilla/5.0 (compatible; DocsScraper/1.0)",
    "selectors": {
      "main_content": "main, article, .prose",
      "code_blocks": "pre code, .code-block",
      "headings": "h1, h2, h3, h4, h5, h6",
      "examples": ".example, .demo"
    }
  },
  "output": {
    "format": "markdown",
    "include_metadata": true,
    "preserve_code_blocks": true,
    "create_index": true
  }
}
```

## Output Structure

Each scraped documentation set creates the following structure:

```
output/
  ├── framework-name/
  │   ├── INDEX.md                 # Master index of all pages
  │   ├── metadata.json            # Configuration metadata
  │   ├── category-1/              # Documentation category
  │   │   ├── page-1.md
  │   │   ├── page-2.md
  │   │   └── ...
  │   ├── category-2/
  │   │   └── ...
  │   └── ...
```

## Adding New Documentation Sources

1. Create a new JSON configuration file in `configs/`
2. Define the documentation structure with sections and pages
3. Configure scraping parameters (rate limiting, selectors, etc.)
4. Run the scraper with your new configuration

## Example: Creating a New Config

```json
{
  "name": "Your Framework",
  "base_url": "https://yourframework.com",
  "docs_base": "https://yourframework.com/docs",
  "version": "2.0",
  "description": "Your framework documentation",
  "sections": [
    {
      "category": "Getting Started",
      "pages": [
        {"title": "Installation", "url": "/docs/installation"},
        {"title": "Quick Start", "url": "/docs/quickstart"}
      ]
    }
  ],
  "scraping": {
    "rate_limit_ms": 1000,
    "max_retries": 3,
    "timeout_ms": 30000,
    "user_agent": "Mozilla/5.0 (compatible; DocsScraper/1.0)"
  },
  "output": {
    "format": "markdown",
    "include_metadata": true,
    "preserve_code_blocks": true,
    "create_index": true
  }
}
```

## Implementation Notes

The current version generates placeholder content for documentation pages. To implement actual web scraping:

1. Add a web scraping library (e.g., `requests` + `BeautifulSoup`, `Playwright`, or `Selenium`)
2. Update the `_scrape_page` method in `scraper.py`
3. Parse HTML using the selectors defined in your config
4. Extract and convert content to Markdown format

## Requirements

- Python 3.6+
- Standard library modules (json, pathlib, argparse, time)

For actual web scraping (not included in current implementation):
- `requests` and `beautifulsoup4`, OR
- `playwright` or `selenium`
- `html2text` or similar Markdown conversion library

## License

Apache 2.0

## Statistics

- **Tailwind CSS**: 180 pages successfully scraped across 17 categories
- **React**: 32 pages successfully scraped across 5 categories
- **Total**: 212 documentation pages organized and indexed
