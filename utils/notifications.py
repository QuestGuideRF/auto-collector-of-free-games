from plyer import notification
import platform
class Notifier :
    def __init__ (self ):
        self .system =platform .system ()
    def send_notification (self ,title ,message ):
        try :
            notification .notify (
            title =title ,
            message =message ,
            app_name ='Коллекционер бесплатных игр',
            timeout =10
            )
        except Exception as e :
            print (f"Не удалось отправить уведомление: {e }")