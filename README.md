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

