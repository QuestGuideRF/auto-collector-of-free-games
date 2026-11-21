import time
from selenium .webdriver .common .by import By
from selenium .webdriver .support .ui import WebDriverWait
from selenium .webdriver .support import expected_conditions as EC
from selenium .common .exceptions import TimeoutException ,NoSuchElementException
from utils .browser import BrowserManager
from tqdm import tqdm
class EpicGamesCollector :
    def __init__ (self ,config ):
        self .config =config
        self .platform_name ="Магазин эпических игр"
        self .driver =None
        self .free_games =[]
        self .claimed_games =[]
    def get_free_games (self ):
        try :
            self .driver =BrowserManager .create_driver (
            self .config .get_browser (),
            self .config .get_headless_mode ()
            )
            self .driver .get ("https://store.epicgames.com/ru/free-games")
            time .sleep (3 )
            self ._handle_cookie_banner ()
            free_game_elements =self .driver .find_elements (By .CSS_SELECTOR ,"a[data-testid='ссылка на предложение-карту']")
            for element in free_game_elements [:5 ]:
                try :
                    game_title =element .find_element (By .CSS_SELECTOR ,"span[data-testid='offer-title-info-title']").text
                    price_element =element .find_elements (By .CSS_SELECTOR ,"span[data-comment='Цена']")
                    is_free =False
                    for price in price_element :
                        if 'FREE'in price .text .upper ()or 'БЕСПЛАТНО'in price .text .upper ():
                            is_free =True
                            break
                    if is_free and game_title :
                        self .free_games .append (game_title )
                except NoSuchElementException :
                    continue
            return self .free_games
        except Exception as e :
            raise Exception (f"Ошибка при получении списка игр: {str (e )}")
    def claim_games (self ):
        if not self .free_games :
            return []
        try :
            credentials =self .config .get_platform_credentials ('epic_games')
            if not credentials ['email']or not credentials ['password']:
                print ("Учетные данные Epic Games не настроены")
                return []
            if not self ._login (credentials ['email'],credentials ['password']):
                return []
            time .sleep (3 )
            for game_title in tqdm (self .free_games ,desc ="Добавление игр",unit ="игра"):
                try :
                    self .driver .get ("https://store.epicgames.com/ru/free-games")
                    time .sleep (2 )
                    game_links =self .driver .find_elements (By .CSS_SELECTOR ,"a[data-testid='ссылка на предложение-карту']")
                    for link in game_links :
                        try :
                            title =link .find_element (By .CSS_SELECTOR ,"span[data-testid='offer-title-info-title']").text
                            if title ==game_title :
                                link .click ()
                                break
                        except :
                            continue
                    time .sleep (3 )
                    try :
                        get_button =WebDriverWait (self .driver ,10 ).until (
                        EC .element_to_be_clickable ((By .XPATH ,"//button[contains(., 'Получить') или contains(., 'Get')]"))
                        )
                        get_button .click ()
                        time .sleep (2 )
                        try :
                            place_order_button =WebDriverWait (self .driver ,5 ).until (
                            EC .element_to_be_clickable ((By .XPATH ,"//button[contains(., 'Оформить заказ') or contains(., 'Place Order')]"))
                            )
                            place_order_button .click ()
                            time .sleep (2 )
                            self .claimed_games .append (game_title )
                        except TimeoutException :
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
            self .driver .get ("https://www.epicgames.com/id/login")
            time .sleep (3 )
            email_input =WebDriverWait (self .driver ,10 ).until (
            EC .presence_of_element_located ((By .ID ,"email"))
            )
            email_input .send_keys (email )
            password_input =self .driver .find_element (By .ID ,"password")
            password_input .send_keys (password )
            login_button =self .driver .find_element (By .ID ,"sign-in")
            login_button .click ()
            time .sleep (5 )
            if "id/login"not in self .driver .current_url :
                return True
            else :
                print ("Не удалось войти в аккаунт Epic Games")
                return False
        except Exception as e :
            print (f"Ошибка авторизации: {str (e )}")
            return False
    def _handle_cookie_banner (self ):
        try :
            cookie_button =WebDriverWait (self .driver ,5 ).until (
            EC .element_to_be_clickable ((By .XPATH ,"//button[contains(text(), 'Принять') or contains(text(), 'Accept')]"))
            )
            cookie_button .click ()
            time .sleep (1 )
        except :
            pass