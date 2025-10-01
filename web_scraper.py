import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from urllib.parse import urljoin, urlparse
import logging

class WebScraper:
    def __init__(self, delay=1):
        """
        Initialize the web scraper
        
        Args:
            delay (int): Delay between requests in seconds
        """
        self.session = requests.Session()
        self.delay = delay
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_page(self, url):
        """
        Fetch a web page
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_links(self, soup, base_url):
        """
        Extract all links from a page
        
        Args:
            soup: BeautifulSoup object
            base_url (str): Base URL for relative links
            
        Returns:
            list: List of absolute URLs
        """
        links = []
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, link['href'])
            links.append(absolute_url)
        return links
    
    def extract_text_content(self, soup):
        """
        Extract clean text content from a page
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            dict: Dictionary with title and text content
        """
        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'title': title_text,
            'content': text
        }
    
    def scrape_single_page(self, url):
        """
        Scrape a single page and return structured data
        
        Args:
            url (str): URL to scrape
            
        Returns:
            dict: Scraped data
        """
        soup = self.get_page(url)
        if not soup:
            return None
        
        data = {
            'url': url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            **self.extract_text_content(soup)
        }
        
        return data
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Data saved to {filename}")
    
    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        if not data:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        self.logger.info(f"Data saved to {filename}")


def main():
    """Example usage of the web scraper"""
    scraper = WebScraper(delay=1)
    
    # Example: Scrape a single page
    url = "https://httpbin.org/html"  # Safe test URL
    
    print("Scraping single page...")
    data = scraper.scrape_single_page(url)
    
    if data:
        print(f"Title: {data['title']}")
        print(f"Content preview: {data['content'][:200]}...")
        
        # Save results
        scraper.save_to_json([data], 'scraped_data.json')
        scraper.save_to_csv([data], 'scraped_data.csv')
    else:
        print("Failed to scrape the page")


if __name__ == "__main__":
    main()