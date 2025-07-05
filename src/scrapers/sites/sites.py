from .AmazonScraper import AmazonScraper
from .FlipkartScraper import FlipkartScraper
from src.driver.driver import Driver
from typing import Type

# only these sites are allowed to scrape from input urls
# if you want to add more sites, just add the site name and handler class in the mapping below
# Note: the site name should be in lowercase and should match the site name in the URL
# Currently we are not validating the domain like "amazon.in" or "amazon.com" etc.
# We are just checking if the site name is present in the URL.
SitesMapping: dict[str, Type[Driver]] = {
    # site name: handler
    "amazon": AmazonScraper,
    "flipkart": FlipkartScraper,
    # add more if needed
}