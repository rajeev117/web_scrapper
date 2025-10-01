# Python Web Scraper

A flexible Python web scraper built with requests and BeautifulSoup.

## Features

- Clean, object-oriented design
- Respectful scraping with delays
- Error handling and logging
- Multiple output formats (JSON, CSV)
- Examples for common scraping scenarios

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from web_scraper import WebScraper

# Create scraper instance
scraper = WebScraper(delay=1)

# Scrape a single page
data = scraper.scrape_single_page("https://example.com")

# Save results
scraper.save_to_json([data], 'results.json')
```

## Usage Examples

### Basic Usage
```bash
python web_scraper.py
```

### Advanced Examples
```bash
python advanced_scraper_example.py
```

## Customization

Modify the CSS selectors in the examples to match your target websites:

```python
# For headlines
headline_selectors = ['h1', 'h2', '.headline', '.title']

# For prices
price_selectors = ['.price', '[class*="price"]']
```

## Best Practices

- Always check robots.txt before scraping
- Use appropriate delays between requests
- Handle errors gracefully
- Respect website terms of service
- Consider using APIs when available

## Legal Notice

This tool is for educational purposes. Always respect website terms of service and robots.txt files.