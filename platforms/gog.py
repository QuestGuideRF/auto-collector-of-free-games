import time
from selenium .webdriver .common .by import By
from selenium .webdriver .support .ui import WebDriverWait
from selenium .webdriver .support import expected_conditions as EC
from selenium .common .exceptions import TimeoutException ,NoSuchElementException
from utils .browser import BrowserManager
from tqdm import tqdm
class GOGCollector :
    def __init__ (self ,config ):
        self .config =config
        self .platform_name ="GOG"
        self .driver =None
        self .free_games =[]
        self .claimed_games =[]
    def get_free_games (self ):
        try :
            self .driver =BrowserManager .create_driver (
            self .config .get_browser (),
            self .config .get_headless_mode ()
            )
            self .driver .get ("https://www.gog.com/games?priceRange=0,0&page=1")
            time .sleep (3 )
            self ._handle_cookie_banner ()
            try :
                game_elements =WebDriverWait (self .driver ,10 ).until (
                EC .presence_of_all_elements_located ((By .CSS_SELECTOR ,"a.product-tile"))
                )
                for element in game_elements [:10 ]:
                    try :
                        title_element =element .find_element (By .CSS_SELECTOR ,"div.product-tile__title")
                        game_title =title_element .get_attribute ("title")
                        if not game_title :
                            game_title =title_element .text
                        if game_title and game_title not in self .free_games :
                            self .free_games .append (game_title )
                    except NoSuchElementException :
                        continue
            except TimeoutException :
                pass
            self .driver .get ("https://www.gog.com/giveaway")
            time .sleep (3 )
            try :
                giveaway_title =self .driver .find_element (By .CSS_SELECTOR ,"h1.giveaway-banner__title")
                game_title =giveaway_title .text .strip ()
                if game_title and game_title not in self .free_games :
                    self .free_games .append (game_title )
            except NoSuchElementException :
                pass
            return self .free_games
        except Exception as e :
            raise Exception (f"Ошибка при получении списка игр: {str (e )}")
    def claim_games (self ):
        if not self .free_games :
            return []
        try :
            credentials =self .config .get_platform_credentials ('gog')
            if not credentials ['email']or not credentials ['password']:
                print ("Учетные данные GOG не настроены")
                return []
            if not self ._login (credentials ['email'],credentials ['password']):
                return []
            time .sleep (3 )
            self .driver .get ("https://www.gog.com/giveaway")
            time .sleep (3 )
            try :
                claim_button =WebDriverWait (self .driver ,10 ).until (
                EC .element_to_be_clickable ((By .CSS_SELECTOR ,"button.giveaway-banner__button"))
                )
                giveaway_title =self .driver .find_element (By .CSS_SELECTOR ,"h1.giveaway-banner__title")
                game_title =giveaway_title .text .strip ()
                claim_button .click ()
                time .sleep (3 )
                self .claimed_games .append (game_title )
            except TimeoutException :
                pass
            for game_title in tqdm (self .free_games ,desc ="Обработка игр",unit ="игра"):
                if game_title not in self .claimed_games :
                    try :
                        self .driver .get ("https://www.gog.com/games?priceRange=0,0&page=1")
                        time .sleep (2 )
                        game_links =self .driver .find_elements (By .CSS_SELECTOR ,"a.product-tile")
                        for link in game_links :
                            try :
                                title =link .find_element (By .CSS_SELECTOR ,"div.product-tile__title").get_attribute ("title")
                                if title ==game_title :
                                    link .click ()
                                    time .sleep (2 )
                                    break
                            except :
                                continue
                        try :
                            add_button =WebDriverWait (self .driver ,5 ).until (
                            EC .element_to_be_clickable ((By .CSS_SELECTOR ,"button.productcard-buy__add-button"))
                            )
                            add_button .click ()
                            time .sleep (2 )
                            self .claimed_games .append (game_title )
                        except TimeoutException :
                            pass
                    except Exception :
                        continue
            return self .claimed_games
        finally :
            if self .driver :
                self .driver .quit ()
    def _login (self ,email ,password ):
        try :
            self .driver .get ("https://login.gog.com/")
            time .sleep (3 )
            email_input =WebDriverWait (self .driver ,10 ).until (
            EC .presence_of_element_located ((By .ID ,"login_username"))
            )
            email_input .send_keys (email )
            password_input =self .driver .find_element (By .ID ,"login_password")
            password_input .send_keys (password )
            login_button =self .driver .find_element (By .ID ,"login_login")
            login_button .click ()
            time .sleep (5 )
            if "login.gog.com"not in self .driver .current_url :
                return True
            else :
                print ("Не удалось войти в аккаунт GOG")
                return False
        except Exception as e :
            print (f"Ошибка авторизации: {str (e )}")
            return False
    def _handle_cookie_banner (self ):
        try :
            cookie_button =WebDriverWait (self .driver ,5 ).until (
            EC .element_to_be_clickable ((By .CSS_SELECTOR ,"button.cookie-accept"))
            )
            cookie_button .click ()
            time .sleep (1 )
        except :
            pass