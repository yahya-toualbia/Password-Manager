# =========================
# auth.py
# =========================
import bcrypt

class AuthManager:

    def __init__(self ,db):
        """
        Initialize authentication manager.
        """
        self.data = db
        self.islogin = False
        self.current_user = None
        self.current_user_id = None

    def register(self, username, password):
        """
        Create new account.
        """
        user = self.data.get_user_by_username(username)
        if user:
            return False
        self.data.create_user(username, self.hash_master_password(password))
        return True
        

    def login(self, username, password):
        """
        Authenticate user login.
        """
        user = self.data.get_user_by_username(username)
        if user:
            if self.verify_master_password(password ,user[2]):
                self.current_user_id = user[0]
                self.current_user = user[1]
                self.islogin = True
                return True
            return False
        return False
        

    def logout(self):
        """
        Logout current user.
        """
        self.islogin = False
        self.current_user = None
        self.current_user_id = None

    def hash_master_password(self, password):
        """
        Hash master password securely.
        """
        
        hashing = bcrypt.hashpw(password.encode() ,bcrypt.gensalt()).decode()

        return hashing 

    def verify_master_password(self, password, hashed_password):
        """
        Verify entered password against stored hash.
        """
        if bcrypt.checkpw(password.encode() ,hashed_password.encode()):
            return True
        return False


    def is_authenticated(self):
        """
        Check if user is logged in.
        """
        return self.islogin

