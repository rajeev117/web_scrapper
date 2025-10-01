from web_scraper import WebScraper
import time

def scrape_news_headlines_example():
    """
    Example: Scrape news headlines from a news website
    This is a template - modify the selectors for your target site
    """
    scraper = WebScraper(delay=2)
    
    # Example URL - replace with your target site
    url = "https://httpbin.org/html"
    
    soup = scraper.get_page(url)
    if not soup:
        return
    
    # Example selectors - modify these for your target site
    headlines = []
    
    # Look for common headline patterns
    headline_selectors = [
        'h1', 'h2', 'h3',
        '.headline', '.title',
        '[class*="headline"]', '[class*="title"]'
    ]
    
    for selector in headline_selectors:
        elements = soup.select(selector)
        for element in elements:
            text = element.get_text().strip()
            if text and len(text) > 10:  # Filter out short/empty text
                headlines.append({
                    'headline': text,
                    'selector': selector,
                    'url': url
                })
    
    return headlines

def scrape_product_info_example():
    """
    Example: Scrape product information
    Template for e-commerce sites
    """
    scraper = WebScraper(delay=1)
    
    # Example product URLs
    urls = [
        "https://httpbin.org/html",
        # Add more URLs here
    ]
    
    products = []
    
    for url in urls:
        soup = scraper.get_page(url)
        if not soup:
            continue
        
        # Example product data extraction
        product = {
            'url': url,
            'title': '',
            'price': '',
            'description': '',
            'images': []
        }
        
        # Title extraction (modify selectors for your site)
        title_selectors = ['h1', '.product-title', '[class*="title"]']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                product['title'] = title_elem.get_text().strip()
                break
        
        # Price extraction
        price_selectors = ['.price', '[class*="price"]', '[data-price]']
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                product['price'] = price_elem.get_text().strip()
                break
        
        # Description
        desc_selectors = ['.description', '[class*="description"]', 'p']
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                product['description'] = desc_elem.get_text().strip()[:500]
                break
        
        # Images
        img_elements = soup.find_all('img')
        for img in img_elements:
            if img.get('src'):
                product['images'].append(img['src'])
        
        products.append(product)
    
    return products

def scrape_with_pagination_example():
    """
    Example: Handle pagination
    """
    scraper = WebScraper(delay=2)
    base_url = "https://httpbin.org/html"
    
    all_data = []
    page = 1
    max_pages = 5  # Safety limit
    
    while page <= max_pages:
        # Construct URL with page parameter
        url = f"{base_url}?page={page}"
        
        soup = scraper.get_page(url)
        if not soup:
            break
        
        # Extract data from current page
        page_data = scraper.extract_text_content(soup)
        page_data['page'] = page
        page_data['url'] = url
        all_data.append(page_data)
        
        # Check if there's a next page
        next_link = soup.find('a', text='Next')
        if not next_link:
            break
        
        page += 1
    
    return all_data

if __name__ == "__main__":
    print("Running advanced scraper examples...")
    
    # Example 1: Headlines
    print("\n1. Scraping headlines...")
    headlines = scrape_news_headlines_example()
    if headlines:
        for headline in headlines[:3]:  # Show first 3
            print(f"- {headline['headline']}")
    
    # Example 2: Products
    print("\n2. Scraping product info...")
    products = scrape_product_info_example()
    if products:
        for product in products[:2]:  # Show first 2
            print(f"Product: {product['title']}")
            print(f"Price: {product['price']}")
    
    # Example 3: Pagination
    print("\n3. Scraping with pagination...")
    paginated_data = scrape_with_pagination_example()
    print(f"Scraped {len(paginated_data)} pages")
    
    # Save all results
    scraper = WebScraper()
    scraper.save_to_json({
        'headlines': headlines,
        'products': products,
        'paginated_data': paginated_data
    }, 'advanced_scraping_results.json')