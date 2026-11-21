import os
import sys
import time
import schedule
from colorama import init ,Fore ,Style
from tqdm import tqdm
from utils .config import Config
from utils .notifications import Notifier
from platforms .epic_games import EpicGamesCollector
from platforms .steam import SteamCollector
from platforms .gog import GOGCollector
init (autoreset =True )
class FreeGamesBot :
    def __init__ (self ):
        self .config =Config ()
        self .notifier =Notifier ()
        self .collectors =[]
        self .init_collectors ()
    def init_collectors (self ):
        platforms =self .config .get_enabled_platforms ()
        if 'epic_games'in platforms :
            self .collectors .append (EpicGamesCollector (self .config ))
        if 'steam'in platforms :
            self .collectors .append (SteamCollector (self .config ))
        if 'gog'in platforms :
            self .collectors .append (GOGCollector (self .config ))
    def print_banner (self ):
        banner =f
        print (banner )
    def collect_games (self ):
        self .print_banner ()
        all_found_games =[]
        all_claimed_games =[]
        total_collectors =len (self .collectors )
        for idx ,collector in enumerate (self .collectors ,1 ):
            print (f"\n{Fore .YELLOW }[{idx }/{total_collectors }] Проверка {collector .platform_name }...{Style .RESET_ALL }")
            try :
                found_games =collector .get_free_games ()
                if found_games :
                    print (f"{Fore .GREEN }Найдено бесплатных игр: {len (found_games )}{Style .RESET_ALL }")
                    for game in found_games :
                        print (f"  • {game }")
                    all_found_games .extend (found_games )
                    claimed =collector .claim_games ()
                    all_claimed_games .extend (claimed )
                    if claimed :
                        print (f"{Fore .GREEN }Успешно добавлено: {len (claimed )} игр(ы){Style .RESET_ALL }")
                    else :
                        print (f"{Fore .YELLOW }Не удалось добавить игры (возможно уже в библиотеке){Style .RESET_ALL }")
                else :
                    print (f"{Fore .YELLOW }Бесплатных игр не найдено{Style .RESET_ALL }")
            except Exception as e :
                print (f"{Fore .RED }Ошибка при работе с {collector .platform_name }: {str (e )}{Style .RESET_ALL }")
                continue
        self .print_summary (all_found_games ,all_claimed_games )
        if all_claimed_games and self .config .get_notifications_enabled ():
            self .notifier .send_notification (
            "Новые бесплатные игры!",
            f"Добавлено {len (all_claimed_games )} игр(ы): {', '.join (all_claimed_games [:3 ])}"
            )
    def print_summary (self ,found_games ,claimed_games ):
        print (f"\n{Fore .CYAN }{'='*60 }")
        print ("ИТОГИ:")
        print (f"{'='*60 }{Style .RESET_ALL }")
        print (f"{Fore .YELLOW }Всего найдено: {len (found_games )} игр(ы){Style .RESET_ALL }")
        print (f"{Fore .GREEN }Успешно добавлено: {len (claimed_games )} игр(ы){Style .RESET_ALL }")
        if claimed_games :
            print (f"\n{Fore .GREEN }Добавленные игры:{Style .RESET_ALL }")
            for game in claimed_games :
                print (f"  ✓ {game }")
    def run_scheduled (self ):
        schedule_time =self .config .get_schedule_time ()
        if schedule_time :
            print (f"{Fore .CYAN }Запланировано выполнение каждый день в {schedule_time }{Style .RESET_ALL }")
            schedule .every ().day .at (schedule_time ).do (self .collect_games )
            print (f"{Fore .YELLOW }Бот запущен. Нажмите Ctrl+C для остановки.{Style .RESET_ALL }\n")
            try :
                while True :
                    schedule .run_pending ()
                    time .sleep (60 )
            except KeyboardInterrupt :
                print (f"\n{Fore .YELLOW }Бот остановлен{Style .RESET_ALL }")
        else :
            print (f"{Fore .RED }Расписание не настроено. Выполняется однократный запуск.{Style .RESET_ALL }")
            self .collect_games ()
    def run_once (self ):
        self .collect_games ()
def main ():
    if len (sys .argv )>1 and sys .argv [1 ]=='--schedule':
        bot =FreeGamesBot ()
        bot .run_scheduled ()
    else :
        bot =FreeGamesBot ()
        bot .run_once ()
if __name__ =="__main__":
    main ()