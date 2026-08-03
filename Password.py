# =========================
# password_manager.py
# =========================
import string
import secrets
from Encryption import EncryptionManager as Encryption
from Auth import AuthManager as Auth
import os
from zxcvbn import zxcvbn

class PasswordManager:

    def __init__(self ,auth ,db):
        """
        Initialize password manager system.
        """
        self.db = db
        self.encryption = Encryption()
        self.auth = auth
    def key_getter(self,password_id,master_password):
        salt = self.db.get_salt(password_id)
        if salt:
            key = self.encryption.generate_key(master_password ,salt[0])
            return key
        return None
    def create_password_entry(self ,website,account_username,password, master_password):
        """
        Create and save new password entry.
        """
        if self.auth.is_authenticated():
            salt = os.urandom(16)
            key = self.encryption.generate_key(master_password ,salt)
            encrypted_password = self.encryption.encrypt_password(password,key)
            self.db.add_password(self.auth.current_user_id ,website ,account_username ,encrypted_password ,salt)
            
            return True
        return False

    def show_all_passwords(self,master_password):
        """
        Display all stored passwords.
        """
        if self.auth.is_authenticated():
            passwords = ""
            passwds = self.db.get_all_passwords(self.auth.current_user_id)
            for num , i in enumerate(passwds,start=1):
                passwords += (f"{num}|password ID: {i[0]} -> website : {i[1]} -> password {self.hide_password(i[0], master_password)}\n")
            return passwords
        

    def view_password(self,password_id ,master_password):
        """
        Display one password entry.
        """
        if self.auth.is_authenticated():
            password = self.db.get_password_by_id(password_id)
            if password:
                key = self.key_getter(password_id ,master_password)
                try:
                    decrypted_password = self.encryption.decrypt_password(password[0] ,key)
                    return decrypted_password
                except:
                    return None
        return None    
    def edit_password(self ,password_id ,new_password ,master_password):
        """
        Edit existing password entry.
        """
        if self.auth.is_authenticated():
            key = self.key_getter(password_id,master_password)
            if key:
                encrypted_new_password = self.encryption.encrypt_password(new_password, key)
                self.db.update_password(password_id ,encrypted_new_password)
                return True
            return False
    def remove_password(self ,password_id):
        """
        Delete password entry.
        """
        if self.auth.is_authenticated():
            self.db.delete_password(password_id)
            
            return True

    def search_passwords(self, website):
        """
        Search saved passwords.
        """
        if self.auth.is_authenticated():
            return self.db.search_by_website(self.auth.current_user_id, website)
        return None

    def generate_password(self, length):
        """
        Generate strong random password.
        """
        #create the password
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(chars) for i in range(length))
        return password

    def check_password_strength(self, password):
        """
        Analyze password strength.
        """
        resalt = zxcvbn(password)
        score = resalt["score"]
        if score == 0:
            return "very weak password"
        elif score == 1:
            return "weak password"
        elif score == 2:
            return "Medium password"
        elif score == 3:
            return "strong password"
        elif score == 4:
            return "very strong password"

    def hide_password(self ,password_id ,master_password):
        """
        Hide password characters.
        """
        pw = self.view_password(password_id ,master_password)
        return "*" * len(pw) if pw else "N/A"

    def reveal_password(self ,password_id, master_password):
        """
        Reveal hidden password.
        """
        return self.view_password(password_id,master_password)
    def close(self):
        self.db.close_connection()