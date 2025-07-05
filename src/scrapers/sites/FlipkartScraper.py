import re
from src.driver.driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

"""
Example usage:
    url = "https://www.flipkart.com/my-gita-original-copy/p/itm7635718d8c3f6?pid=9788129137708"
    flipkart = FlipkartScraper(url)
    product_details = flipkart.get_product_details()
    print("product_details:", product_details)
"""
class FlipkartScraper(Driver):
    url: str = ""
    site_name: str = ""

    def __init__(self, url: str, site_name: str=""):
        super().__init__()
        self.url = url
        self.site_name = site_name
        self.driver = self.get_driver()
        self.wait = self.get_driverWait()
        self.driver.get(url)

    def get_product_details(self) -> dict[str, str | list[str]]:
        error_flags = [] # to keep track of any errors encountered during scraping
        product_name = ""
        price = ""
        currency=""
        availability=0

        # Close login popup if present
        try:
            close_login = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"✕")]')))
            close_login.click()
        except:
            pass  # popup did not appear

        # Product Name
        try:
            # Wait for the product title to be present and retrieve it
            product_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.C7fEHH h1._6EBuvT span.VU-ZEz"))).text.strip()
        except:
            error_flags.append("product_name")

        # assuming that once product_name is found that means the page has loaded with the product details
        # and we can proceed to scrape the rest of the details

        # Price and Currency
        try:
            currency_price = self.driver.find_element(By.CSS_SELECTOR, "div.C7fEHH div.hl05eU div.Nx9bqj.CxhGGd").text.strip()
            match = re.match(r"([^\d]+)?([\d,.]+)", currency_price.strip())
            if match:
                currency = match.group(1).strip() if match.group(1) else ""
                price = match.group(2).replace(",", "")
            else:
                print("No match found currency_price.")
                error_flags.append("price")
                error_flags.append("currency")
        except:
            error_flags.append("price")
            error_flags.append("currency")


        # Availability
        try:
            availability = self.driver.find_element(By.CSS_SELECTOR, "div.DOjaWF div.cPHDOP div.Z8JjpR").text.strip() # it will return "Sold Out"
            # it can throw the error if the element is not found so it mean the product is in stock
            if availability.lower().startswith("sold out"):
                availability = 0
            else:
                availability = 1
        except:
            availability = 1

        
        data = {
            "site_name": self.site_name,
            "product_name": product_name,
            "currency": currency,
            "price": price,
            "availability": availability,
            "url": self.url,
            # "error_flags": error_flags
        }

        self.quit() # closing the driver after scraping

        return data

    