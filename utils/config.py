import os
import json
from utils .encryption import Encryption
class Config :
    def __init__ (self ,config_path ='config.json'):
        self .config_path =config_path
        self .encryption =Encryption ()
        self .config =self .load_config ()
    def load_config (self ):
        if not os .path .exists (self .config_path ):
            self .create_default_config ()
        with open (self .config_path ,'r',encoding ='utf-8')as f :
            return json .load (f )
    def create_default_config (self ):
        default_config ={
        "platforms":{
        "epic_games":{
        "enabled":True ,
        "email":"",
        "password":""
        },
        "steam":{
        "enabled":False ,
        "username":"",
        "password":""
        },
        "gog":{
        "enabled":False ,
        "email":"",
        "password":""
        }
        },
        "settings":{
        "headless":False ,
        "schedule_time":"10:00",
        "notifications":True ,
        "browser":"chrome"
        }
        }
        with open (self .config_path ,'w',encoding ='utf-8')as f :
            json .dump (default_config ,f ,indent =4 ,ensure_ascii =False )
        print (f"Создан файл конфигурации: {self .config_path }")
        print ("Пожалуйста, заполните данные для входа в config.json")
        return default_config
    def get_platform_credentials (self ,platform ):
        platform_config =self .config ['platforms'].get (platform ,{})
        email =platform_config .get ('email','')
        password =platform_config .get ('password','')
        username =platform_config .get ('username','')
        if password and not password .startswith ('encrypted:'):
            encrypted_password =self .encryption .encrypt (password )
            platform_config ['password']=f"encrypted:{encrypted_password }"
            self .save_config ()
            password =encrypted_password
        elif password .startswith ('encrypted:'):
            password =password .replace ('encrypted:','')
        decrypted_password =self .encryption .decrypt (password )if password else ''
        return {
        'email':email ,
        'username':username ,
        'password':decrypted_password
        }
    def save_config (self ):
        with open (self .config_path ,'w',encoding ='utf-8')as f :
            json .dump (self .config ,f ,indent =4 ,ensure_ascii =False )
    def get_enabled_platforms (self ):
        enabled =[]
        for platform ,config in self .config ['platforms'].items ():
            if config .get ('enabled',False ):
                enabled .append (platform )
        return enabled
    def get_headless_mode (self ):
        return self .config ['settings'].get ('headless',False )
    def get_schedule_time (self ):
        return self .config ['settings'].get ('schedule_time','')
    def get_notifications_enabled (self ):
        return self .config ['settings'].get ('notifications',True )
    def get_browser (self ):
        return self .config ['settings'].get ('browser','chrome')