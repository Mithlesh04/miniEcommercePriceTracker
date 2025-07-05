import pandas as pd
from src.scrapers.scraper import Scraper

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

    # initialize the Scraper with the list of URLs and the on_complete callback
    Scraper(url_list, on_complete=on_complete)