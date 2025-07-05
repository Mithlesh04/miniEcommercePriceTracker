from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

urls = [
    "https://www.amazon.in/COVALENT-Chemistry-Shortcuts-Mechanisms-Reactions/dp/B0FF9VFPM6",
    "https://www.flipkart.com/my-gita-original-copy/p/itm7635718d8c3f6?pid=9788129137708",
    # "https://www.amazon.in/",
    # "https://amazon.inw",
    # "https://www.flipkat.com/"
]

executable_path = "./driver/138.0.7204.0/chromedriver-win64/chromedriver.exe"

def getdriver():
    # Chrome options
    options = Options()
    options.add_argument("--headless")  # run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(executable_path=executable_path)

    # Path to your chromedriver

    # Start driver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

