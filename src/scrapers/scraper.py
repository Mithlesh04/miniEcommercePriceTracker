import random
import time
import re
from typing import Callable
from urllib.parse import urlparse
from sites.sites import SitesMapping
from concurrent.futures import ThreadPoolExecutor, wait


class Scraper:
    data: list[dict | None] = []
    group_urls: dict[str, list[str]] = {}
    MAX_THREAD_WORKERS = 5  # Maximum number of concurrent threads
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
    
    def _process_sites(self) -> None:
        all_futures = []
        for site_name in self.group_urls:
            site_urls = self.group_urls[site_name]
            """
                Concurrency Strategy: Parallel vs Sequential
                
                Current implementation: **Concurrent with random delays**
                --------------------------------------------------------
                We are using a *Thread Pool Executor* with `max_workers = self.MAX_THREAD_WORKERS{5}`.
                This means up to self.MAX_THREAD_WORKERS{5} threads (workers) will process URLs concurrently.
            
                For each thread, a random wait time (2–5 seconds) is added **before** scraping starts.
                Once any thread finishes its task, it picks up the next URL from the queue.
            
                This is called: **Concurrent Processing with Random Delay per Task**
                or simply **Parallel Scraping with Delay per Thread**.
            
                Example:
                ----------
                URLs: [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
                Threads: 5
                Each of the first 5 URLs is assigned to one thread, waits randomly 2–5s, then proceeds.
                As threads finish, remaining URLs are picked up.
            
            
                Alternative implementation: **Sequential with random delays**
                -------------------------------------------------------------
                In some cases (if the server is very sensitive to concurrency or blocking),
                you may want to scrape *one URL at a time*, waiting randomly (2–5s) between each request.
            
                This is called: **Sequential Processing with Random Delay between Tasks**
                or simply **Serial Scraping with Delay**.
            
                Example:
                ----------
                URLs: [u1, u2, u3, u4, u5, ...]
                Process u1 → wait 2–5s → process u2 → wait 2–5s → … one at a time.
            
                Which strategy to use depends on:
                - Site rate-limits & anti-bot policies
                - Your hardware capacity
                - How fast you need results
            
                Currently we are using: **Concurrent Processing with Random Delay per Task**
                
                Note: This is for list of same site URLs.
            """
            with ThreadPoolExecutor(max_workers=min(self.MAX_THREAD_WORKERS, len(site_urls))) as executor:
                for url in site_urls:
                    future = executor.submit(self._process_scraping, site_name, url)
                    all_futures.append(future)
                    # currently not doing any error handing

        # Wait until all tasks are done
        wait(all_futures)

        # Once all tasks are done, we can call the completion handler
        self._on_all_process_complete()
     
    def _process_scraping(self, site_name: str, url: str) -> None:
        wait_time = random.randint(2, 5)  # random wait time between 2 and 5
        time.sleep(wait_time)

        # calling main scraper handler
        scraper_handler = SitesMapping[site_name](url, site_name)
        product_details = scraper_handler.get_product_details()

        # adding more data
        product_details["site"] = site_name
        product_details["url"] = url

        self.data.append(product_details)        

    def _on_all_process_complete(self) -> None:
        print(f"Finished scraping")
        if callable(self.on_complete):
            print("on_complete function triggered")
            self.on_complete(self.data)