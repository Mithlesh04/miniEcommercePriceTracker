import random
import time
import re
from typing import Callable
from urllib.parse import urlparse
from .sites.sites import SitesMapping
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime


class Scraper:
    data: list[dict | None] = []
    group_urls: dict[str, list[str]] = {}
    MAX_THREAD_WORKERS = 1  # Maximum number of concurrent threads
    on_complete: Callable[[list[dict | None]], None]

    def __init__(self, urls: list[str], on_complete: Callable[[list[dict | None]], None]):
        self.urls = urls
        self.on_complete = on_complete
        self._group_urls_by_scraper(urls)
        self._process_sites()

    # it will group all the urls by site name 
    # ex, { amazon: ["https://amazon.inw", "https://amazon.in"], "flipkart": ["https://www.flipkat.com/"] }
    def _group_urls_by_scraper(self, urls) -> None:
        for url in urls:
            if isinstance(url, str):
                parsed = urlparse(url)
                host = parsed.netloc.lower()
                # check if this site name is allowed to scrape
                for site_name in SitesMapping:
                    if re.match(rf"^(.*\.)?{re.escape(site_name.lower())}(\.|$)", host) is not None:
                        if not site_name in self.group_urls:
                            self.group_urls[site_name] = []
                        
                        self.group_urls[site_name].append(url)
                        break
    
    """
    @_process_sites
    ----------------

    What we are doing here:
        We scrape a list of product URLs efficiently by:

        Grouping URLs by site (e.g., Amazon, Flipkart).

        For each group:
            We run a separate thread pool (ThreadPoolExecutor) for that site group.
            Inside each pool, we process multiple URLs of that site concurrently, up to MAX_THREAD_WORKERS.
            Each URL waits randomly (2–5s) before scraping, to avoid detection.
            All site groups (Amazon, Flipkart, etc.) are also processed in parallel, so no group waits for another.
    """ 
    def _process_sites(self) -> None:
        with ThreadPoolExecutor(max_workers=len(self.group_urls)) as group_executor:
            wait([group_executor.submit(self._group_site_executor, site_name, self.group_urls[site_name]) for site_name in self.group_urls])

        # Once all tasks are done, we can call the completion handler
        self._on_all_process_complete()
    
    def _group_site_executor(self, site_name: str, site_urls: list[str]) -> None:
        with ThreadPoolExecutor(max_workers=min(self.MAX_THREAD_WORKERS, len(site_urls))) as executor:
            wait([executor.submit(self._process_scraping, site_name, url) for url in site_urls])

    def _process_scraping(self, site_name: str, url: str) -> None:
        # calling main scraper handler
        scraper_handler = SitesMapping[site_name](url, site_name)
        product_details = scraper_handler.get_product_details()
        product_details["availability"] = "In stock" if product_details.get("availability", 0) else "Out of stock"

        # ONLY FOR TESTING PURPOSES to test concurrency functionality without any scraping
        # add time minutes:seconds:millionseconds to the product details
        # product_details={}
        # product_details['scraped_at'] = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        # product_details["site_name"] = site_name
        # product_details["url"] = url
        
        self.data.append(product_details)
        wait_time = random.randint(2, 5)  # random wait time between 2 and 5
        time.sleep(wait_time)
        

    def _on_all_process_complete(self) -> None:
        print(f"Finished scraping")
        if callable(self.on_complete):
            print("on_complete function triggered")
            self.on_complete(self.data)