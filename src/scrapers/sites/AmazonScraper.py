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

    def __init__(self, url: str, site_name: str=""):
        super().__init__()
        self.url = url
        self.site_name = site_name
        self.driver = self.get_driver()
        self.wait = self.get_driverWait()
        self.driver.get(url)

    def get_product_details(self) -> dict[str, str | list[str]]:
        # use the webdriver for better handling the page loading
        # currently this is hardcoded to wait for 3 seconds as Amazon pages can take time to load.
        # self.driver.implicitly_wait(3)  # wait for elements to load

        error_flags = [] # to keep track of any errors encountered during scraping
        product_name = ""
        price = ""
        currency=""
        availability=0

        # Product Name
        try:
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

        
        data = {
            "site_name": self.site_name,
            "product_name": product_name,
            "currency": currency,
            "price": price,
            "availability": availability,
            "url": self.url,
            # "error_flags": error_flags
        }


        if data["product_name"] == "":
            # if product name is still not found, we will save the HTML for debugging
            save_page_html(self.url, self.driver.page_source)

        self.quit() # closing the driver after scraping

        return data

    