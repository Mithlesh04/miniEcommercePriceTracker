from src.driver.driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.utils.save_page_html import save_page_html



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
    data: dict[str, str | list[str]] = {}

    def __init__(self, url: str, site_name: str=""):
        super().__init__()
        self.url = url
        self.site_name = site_name
        self.fetch_url_content()

    def fetch_url_content(self) -> None:
        """Fetch the content of the URL."""
        self.driver = self.get_driver()
        self.wait = self.get_driverWait()
        self.driver.get(self.url)
        self.wait_for_page_load()
    
    def get_product_details(self) -> dict[str, str | list[str]]:
        error_flags = [] # to keep track of any errors encountered during scraping
        product_name = ""
        price = ""
        currency=""
        availability=0

        # Product Name
        try:
            print("Waiting for product name element...Amazon")

            self.wait_for_element(By.ID, "productTitle")
            product_name = self.wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text.strip()
        except:
            error_flags.append("product_name")

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

        
        self.data = {
            "site_name": self.site_name,
            "product_name": product_name,
            "currency": currency,
            "price": price,
            "availability": availability,
            "url": self.url,
            # "error_flags": error_flags
        }


        if self.data["product_name"] == "":            
            print("------------Error: Product name not found in Amazon!------------")
            # if product name is still not found, we will save the HTML for debugging in respective of retry count
            save_page_html(self.url, self.driver.page_source, self.site_name)

        self.quit() # closing the driver after scraping

        return self.data

    