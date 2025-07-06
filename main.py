import pandas as pd
from src.scrapers.scraper import Scraper
from src.scrapers.sites.FlipkartScraper import FlipkartScraper
from src.utils.save_page_html import save_page_html

PRODUCT_URL_FILE = './product_urls.txt'
FILE_TO_SAVE_SCRAPED_DATA = './scraped_prices.csv'

# function to read product URLs from a PRODUCT_URL_FILE
def get_product_urls():
    df = pd.read_csv(PRODUCT_URL_FILE, header=None, names=['url'])
    url_list = df['url'].tolist()
    return url_list


url_list = get_product_urls()

def on_complete(data: list[dict | None]):
    # Convert results to DataFrame
    df = pd.DataFrame(data)
    # Save DataFrame to CSV
    df.to_csv(FILE_TO_SAVE_SCRAPED_DATA, index=False)


if __name__ == "__main__":

    # url =  "https://www.flipkart.com/lenovo-ultra-7-155h-wuxga-oled-intel-core-16-gb-1-tb-ssd-windows-11-home-14imh9-thin-light-laptop/p/itm77304edff3814?pid=COMH3G969EWNAHYG&lid=LSTCOMH3G969EWNAHYGM4NHIP&marketplace=FLIPKART&q=laptop&store=6bo%2Fb5g&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=017ca714-4ca1-4264-b8c6-30362a80e6c7.COMH3G969EWNAHYG.SEARCH&ppt=sp&ppn=sp&ssid=8w6qqkoo7k0000001751730561076&qH=312f91285e048e09"
    # Example usage of FlipkartScraper
    # flipkart_scraper = FlipkartScraper(url, site_name="Flipkart")
    # product_details = flipkart_scraper.get_product_details()
    # print("Product Details:", product_details)

    # save_page_html(url, "<html>Sample HTML content for testing</html>", site_name="Flipkart")
    # initialize the Scraper with the list of URLs and the on_complete callback
    Scraper(url_list, on_complete=on_complete)
    pass