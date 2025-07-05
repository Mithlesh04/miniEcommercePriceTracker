from driver.driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

"""
Example usage:
    url = "https://www.amazon.in/COVALENT-Chemistry-Shortcuts-Mechanisms-Reactions/dp/B0FF9VFPM6"
    amazon = AmazonScraper(url)
    product_details = amazon.get_product_details()
    print("product_details:", product_details)
"""
class AmazonScraper(Driver):
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

        # Product Name
        try:
            # Wait for the product title to be present and retrieve it
            product_name = self.wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text.strip()
        except:
            error_flags.append("product_name")

        # assuming that once product_name is found that means the page has loaded with the product details
        # and we can proceed to scrape the rest of the details

        # Price and Currency
        try:
            currency = self.driver.find_element(By.CSS_SELECTOR, 'span.a-price span.a-price-symbol').text.strip()
            price = self.driver.find_element(By.CSS_SELECTOR, 'span.a-price span.a-price-whole').text.strip()
        except:
            error_flags.append("price")
            error_flags.append("currency")


        # Availability
        try:
            availability = self.driver.find_element(By.ID, "availability").text.strip()
            if availability.lower().startswith("in stock"):
                availability = 1
            else:
                availability = 0
        except:
            error_flags.append("availability")

        
        data = {
            "site_name": self.site_name,
            "product_name": product_name,
            "price": price,
            "currency": currency,
            "availability": availability,
            "url": self.url,
            # "error_flags": error_flags
        }

        self.quit() # closing the driver after scraping

        return data

    