# Mini Product Price Scraper

This project scrapes product details such as name, price, currency, and availability (1=in stock | 0=sold out) from supported e-commerce websites like Amazon and Flipkart. It uses Python and Selenium with concurrency to speed up scraping.

---

## Setup and Usage

### Create Virtual Environment

Create a virtual environment to isolate dependencies:

Windows:
```bash 
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Assumptions & Info
- The product URLs to scrape are listed in a file named `product_urls.txt` located in the root directory of the project.
- Each URL in `product_urls.txt` is on a separate line without any empty lines.
- There will be no duplicate URLs in the `product_urls.txt` file.
- There will be no huge number of URLs in the `product_urls.txt` file. bcoz,
    - Error handling is not implemented.
    - currently useragent is randomly which means it can repeat in a short time which can lead to failure of scraping.
    - Request rate is controlled by random delays (2–5 seconds) between requests it can lead to blockage if too many URLs are processed in a short time.
    - Data streming to csv is not there currently which means if there are too many URLs, it can lead to memory issues or performance degradation.
    - We are saving csv once all URLs are processed which can lead to data loss if the script fails before saving.
- The URLs in `product_urls.txt` are valid and accessible.
- The script will run in an environment with internet access to fetch product details from the specified URLs.
- Do not keep open the `scraped_prices.csv` when running the script, as it will throw an error if the file is open in write mode.
- The scraped data will be saved in a file named `scraped_prices.csv` in the root directory of the project.


## Working Video
`demo_videos` folder will contain the list of videos like code_walkthrough and working video of project

## Links:
Working Video: https://youtu.be/6Sw0o_Ce9lY
Code Walkthrough: https://youtu.be/F1NbzRnK2Ao



## Error
`error_html_pages` folder will contain the list of error html pages from which we got the error and due to that we were not able to get the product details
This is only for debugging purpose!



## Features

- Reads product URLs from `./product_urls.txt`, one URL per line.
- Supports scraping multiple product URLs from different supported sites (currently: Amazon, Flipkart).
- Fully grouped concurrent scraping:
  - URLs are first grouped by site.
  - Each site group runs its own thread pool, processing URLs concurrently.
  - Site groups themselves are processed in parallel.
- Random delays (2–5 seconds) added before each scrape to mimic human browsing behavior and reduce detection risk.
- Outputs scraped results to `./scraped_prices.csv` in CSV format:
- Python is installed on your system.

---

## Concurrency Behavior

### Current Implementation: Fully Grouped Concurrent Processing
URLs are first grouped by site (e.g., all Amazon URLs together, all Flipkart URLs together).

For each site group, a separate ThreadPoolExecutor with up to MAX_THREAD_WORKERS threads processes URLs concurrently within that group.

Site groups themselves are also processed concurrently — all site groups start at the same time, each in its own thread pool.

**Example:**

Given input URLs:
amazon_url1, flipkart_url1, amazon_url2, amazon_url3, flipkart_url2, amazon_url4

Groups into:
Amazon:    amazon_url1, amazon_url2, amazon_url3, amazon_url4
Flipkart:  flipkart_url1, flipkart_url2

Then starts both groups at the same time:

Amazon URLs processed concurrently (amazon_url1, amazon_url2, …)
Flipkart URLs processed concurrently (flipkart_url1, flipkart_url2)

---
