import os
import base64
from cryptography .fernet import Fernet
from cryptography .hazmat .primitives import hashes
from cryptography .hazmat .primitives .kdf .pbkdf2 import PBKDF2
class Encryption :
    def __init__ (self ):
        self .key_file ='.encryption_key'
        self .key =self .load_or_create_key ()
        self .cipher =Fernet (self .key )
    def load_or_create_key (self ):
        if os .path .exists (self .key_file ):
            with open (self .key_file ,'rb')as f :
                return f .read ()
        else :
            key =Fernet .generate_key ()
            with open (self .key_file ,'wb')as f :
                f .write (key )
            return key
    def encrypt (self ,data ):
        if not data :
            return ''
        encrypted =self .cipher .encrypt (data .encode ())
        return base64 .urlsafe_b64encode (encrypted ).decode ()
    def decrypt (self ,encrypted_data ):
        if not encrypted_data :
            return ''
        try :
            decoded =base64 .urlsafe_b64decode (encrypted_data .encode ())
            decrypted =self .cipher .decrypt (decoded )
            return decrypted .decode ()
        except Exception :
            return ''