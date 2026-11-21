import time
import requests
from selenium .webdriver .common .by import By
from selenium .webdriver .support .ui import WebDriverWait
from selenium .webdriver .support import expected_conditions as EC
from selenium .common .exceptions import TimeoutException ,NoSuchElementException
from utils .browser import BrowserManager
from tqdm import tqdm
class SteamCollector :
    def __init__ (self ,config ):
        self .config =config
        self .platform_name ="Steam"
        self .driver =None
        self .free_games =[]
        self .claimed_games =[]
    def get_free_games (self ):
        try :
            response =requests .get (
            "https://store.steampowered.com/search/",
            params ={
            "maxprice":"free",
            "specials":"1",
            "category1":"998"
            }
            )
            if response .status_code !=200 :
                return []
            self .driver =BrowserManager .create_driver (
            self .config .get_browser (),
            self .config .get_headless_mode ()
            )
            self .driver .get ("https://store.steampowered.com/search/?maxprice=free&specials=1")
            time .sleep (3 )
            self ._handle_age_check ()
            game_elements =self .driver .find_elements (By .CSS_SELECTOR ,"a.search_result_row")[:10 ]
            for element in game_elements :
                try :
                    title_element =element .find_element (By .CSS_SELECTOR ,"span.title")
                    game_title =title_element .text
                    price_elements =element .find_elements (By .CSS_SELECTOR ,"div.discount_final_price")
                    for price in price_elements :
                        if 'Free'in price .text or 'Бесплатно'in price .text or price .text .strip ()=='':
                            if game_title and game_title not in self .free_games :
                                self .free_games .append (game_title )
                            break
                except NoSuchElementException :
                    continue
            return self .free_games
        except Exception as e :
            raise Exception (f"Ошибка при получении списка игр: {str (e )}")
    def claim_games (self ):
        if not self .free_games :
            return []
        try :
            credentials =self .config .get_platform_credentials ('steam')
            if not credentials ['username']or not credentials ['password']:
                print ("Учетные данные Steam не настроены")
                return []
            if not self ._login (credentials ['username'],credentials ['password']):
                return []
            time .sleep (3 )
            for game_title in tqdm (self .free_games ,desc ="Обработка игр",unit ="игра"):
                try :
                    self .driver .get ("https://store.steampowered.com/search/?maxprice=free&specials=1")
                    time .sleep (2 )
                    game_links =self .driver .find_elements (By .CSS_SELECTOR ,"a.search_result_row")
                    for link in game_links :
                        try :
                            title =link .find_element (By .CSS_SELECTOR ,"span.title").text
                            if title ==game_title :
                                game_url =link .get_attribute ('href')
                                self .driver .get (game_url )
                                time .sleep (2 )
                                break
                        except :
                            continue
                    try :
                        play_button =WebDriverWait (self .driver ,5 ).until (
                        EC .element_to_be_clickable ((By .CSS_SELECTOR ,"a.btnv6_blue_hoverfade"))
                        )
                        if 'Play'in play_button .text or 'Играть'in play_button .text :
                            self .claimed_games .append (game_title )
                        else :
                            play_button .click ()
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
    def _login (self ,username ,password ):
        try :
            self .driver .get ("https://store.steampowered.com/login/")
            time .sleep (3 )
            username_input =WebDriverWait (self .driver ,10 ).until (
            EC .presence_of_element_located ((By .CSS_SELECTOR ,"ввод[тип='текст']"))
            )
            username_input .send_keys (username )
            password_input =self .driver .find_element (By .CSS_SELECTOR ,"ввод[тип='пароль']")
            password_input .send_keys (password )
            login_button =self .driver .find_element (By .CSS_SELECTOR ,"кнопка[тип='отправить']")
            login_button .click ()
            time .sleep (5 )
            if "login"not in self .driver .current_url .lower ():
                return True
            else :
                print ("Не удалось войти в аккаунт Steam (возможно требуется 2FA)")
                return False
        except Exception as e :
            print (f"Ошибка авторизации: {str (e )}")
            return False
    def _handle_age_check (self ):
        try :
            age_select =WebDriverWait (self .driver ,3 ).until (
            EC .presence_of_element_located ((By .ID ,"ageYear"))
            )
            age_select .send_keys ("1990")
            view_button =self .driver .find_element (By .CSS_SELECTOR ,"a.btnv6_blue_hoverfade")
            view_button .click ()
            time .sleep (2 )
        except :
            pass