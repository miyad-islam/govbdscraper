import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import json
import time
import os

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.folder_name = base_url.split("://")[1]  # Splits at '://' and takes the second part
        self.folder_path = f"Output/{self.folder_name}"
        self.output_file = f"{self.folder_path}/webscrap.json"
        self.visited_urls_file = f"{self.folder_path}/visited_urls.txt"

        # Configure browser options
        self.driver = self.configure_browser()
        self.visited_urls = set()
        self.all_data = {}

        # Create the folder if it doesn't exist
        os.makedirs(self.folder_path, exist_ok=True)

        # Load existing data
        self.load_data()




    def configure_browser(self):
        """Configure browser to appear more human-like"""
        options = webdriver.EdgeOptions()

        # General browser options
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Set realistic user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")

        # Additional stealth settings
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-save-password-revision")

        driver = webdriver.Edge(options=options)

        return driver

    def load_data(self):
        """Load existing scraped data and visited URLs."""
        if os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0:
            try:
                with open(self.output_file, "r", encoding="utf-8") as f:
                    self.all_data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: webscrap.json contains invalid JSON. Initializing with an empty dictionary.")
                self.all_data = {}
        else:
            self.all_data = {}

        if os.path.exists(self.visited_urls_file) and os.path.getsize(self.visited_urls_file) > 0:
            with open(self.visited_urls_file, "r", encoding="utf-8") as f:
                self.visited_urls = set(f.read().splitlines())
        else:
            self.visited_urls = set()

    def save_data(self):
        """Save the scraped data to the JSON file."""
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, ensure_ascii=False, indent=4)

    def save_visited_urls(self):
        """Save the visited URLs to a text file."""
        with open(self.visited_urls_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.visited_urls))

    def crawl_and_scrape(self, url):
        """Crawl and scrape a given URL."""
        if url in self.visited_urls and url != self.base_url:
            return
        self.visited_urls.add(url)

        try:
            # Visit the URL
            self.driver.get(url)
            print(f"Visiting: {url}")

            # Wait for the page to load completely
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            time.sleep(3)  # Adjust sleep time as needed

            # Scrape the entire page content
            page_content = self.driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")

            # Save the scraped content
            self.all_data[url] = page_content

            # Save data and visited URLs after each page is scraped
            self.save_data()
            self.save_visited_urls()

            # Find all internal links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and self.domain in urlparse(href).netloc:
                    full_url = urljoin(self.base_url, href)
                    if full_url.startswith(self.base_url) and full_url not in self.visited_urls:
                        self.crawl_and_scrape(full_url)
        except Exception as e:
            print(f"Error visiting {url}: {e}")

    def start_crawling(self):
        """Start the crawling process."""
        self.crawl_and_scrape(self.base_url)
        self.driver.quit()
        print("Crawling completed. Data saved to webscrap.json")

    def stop_crawling(self):
        if self.driver:
            self.driver.quit()  # Close the driver