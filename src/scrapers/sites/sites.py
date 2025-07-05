from .AmazonScraper import AmazonScraper
from .FlipkartScraper import FlipkartScraper
from driver.driver import Driver
from typing import Type


SitesMapping: dict[str, Type[Driver]] = {
    # accepted site name: handler
    "amazon": AmazonScraper,
    "flipkart": FlipkartScraper,
    # add more if needed
}