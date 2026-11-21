from selenium import webdriver
from selenium .webdriver .chrome .service import Service as ChromeService
from selenium .webdriver .firefox .service import Service as FirefoxService
from selenium .webdriver .edge .service import Service as EdgeService
from webdriver_manager .chrome import ChromeDriverManager
from webdriver_manager .firefox import GeckoDriverManager
from webdriver_manager .microsoft import EdgeChromiumDriverManager
from selenium .webdriver .chrome .options import Options as ChromeOptions
from selenium .webdriver .firefox .options import Options as FirefoxOptions
from selenium .webdriver .edge .options import Options as EdgeOptions
class BrowserManager :
    @staticmethod
    def create_driver (browser_type ='chrome',headless =False ):
        if browser_type .lower ()=='chrome':
            return BrowserManager ._create_chrome_driver (headless )
        elif browser_type .lower ()=='firefox':
            return BrowserManager ._create_firefox_driver (headless )
        elif browser_type .lower ()=='edge':
            return BrowserManager ._create_edge_driver (headless )
        else :
            return BrowserManager ._create_chrome_driver (headless )
    @staticmethod
    def _create_chrome_driver (headless ):
        options =ChromeOptions ()
        if headless :
            options .add_argument ('--headless=новый')
        options .add_argument ('--no-sandbox')
        options .add_argument ('--disable-dev-shm-usage')
        options .add_argument ('--disable-blink-features=Управление автоматизацией')
        options .add_experimental_option ("excludeSwitches",["enable-automation"])
        options .add_experimental_option ('useAutomationExtension',False )
        options .add_argument ('--disable-gpu')
        options .add_argument ('--window-size=1920,1080')
        options .add_argument ('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, например Gecko) Chrome/120.0.0.0 Safari/537.36')
        service =ChromeService (ChromeDriverManager ().install ())
        driver =webdriver .Chrome (service =service ,options =options )
        driver .execute_script ("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    @staticmethod
    def _create_firefox_driver (headless ):
        options =FirefoxOptions ()
        if headless :
            options .add_argument ('--headless')
        options .set_preference ('dom.webdriver.enabled',False )
        options .set_preference ('useAutomationExtension',False )
        service =FirefoxService (GeckoDriverManager ().install ())
        return webdriver .Firefox (service =service ,options =options )
    @staticmethod
    def _create_edge_driver (headless ):
        options =EdgeOptions ()
        if headless :
            options .add_argument ('--headless=новый')
        options .add_argument ('--no-sandbox')
        options .add_argument ('--disable-dev-shm-usage')
        options .add_argument ('--disable-blink-features=Управление автоматизацией')
        options .add_experimental_option ("excludeSwitches",["enable-automation"])
        options .add_experimental_option ('useAutomationExtension',False )
        service =EdgeService (EdgeChromiumDriverManager ().install ())
        driver =webdriver .Edge (service =service ,options =options )
        driver .execute_script ("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver