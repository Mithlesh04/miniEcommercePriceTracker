import random
from selenium import webdriver
from .user_agents import USER_AGENTS
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


class Driver:
    options = Options()

    """A class to manage the Selenium WebDriver for Chrome."""
    driver: webdriver.Chrome = None

    def __init__(self):
        default_options = [
            "--headless",
            "--window-size=1920,1080",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            # currently it's default rotation inrespect to the site
            # for more improvement we can also use the site map per rotation
            f"user-agent={random.choice(USER_AGENTS)}"
        ]
        # Set default options for the Chrome WebDriver
        self.set_options(default_options)

    def get_driver(self) -> webdriver.Chrome:
        self.driver = webdriver.Chrome(
            # using ChromeDriverManager to automatically manage the driver including installation
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )
        return self.driver
        
    def set_options(self, options=None | list[str]) -> None:
        if isinstance(options, list):
            for option in options:
                self.options.add_argument(option)

    def get_driverWait(self, timeout: int = 10) -> WebDriverWait:
        self.wait = WebDriverWait(self.driver, timeout)
        return self.wait

    def quit(self) -> None:
        self.driver.quit()