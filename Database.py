# =========================
# database.py
# =========================

import sqlite3


class DatabaseManager:

    def __init__(self, db_name="passwords.db"):
        """
        Initialize database settings.
        Store database name and connection variables.
        """
        self.db_name = db_name
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()
        self.create_tables()

    def save_changes(self):
        self.connect.commit()
    def close_connection(self):
        """
        Close database connection safely.
        """
        if self.connect:
            self.connect.close()

    def create_tables(self):
        """
        Create users and passwords tables if they do not exist.
        """
        
        #create the tables
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (password_id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT NOT NULL,
    account_username TEXT NOT NULL,
    encrypted_password BLOB NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    encryption_salt BLOB NOT NULL,
    user_id INTEGER,
    
    FOREIGN KEY(user_id) REFERENCES users(user_id))""")
        

    # =========================
    # Users
    # =========================

    def create_user(self, username, password_hash):
        """
        Insert a new user into database.
        """
        user = (username ,password_hash )
        
        self.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?,?)",user )
        self.save_changes()


    def get_user_by_username(self, username):
        """
        Get user data using username.
        """
        self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
        return self.cursor.fetchone()
        

    def get_user_by_id(self, user_id):
        """
        Get user data using id.
        """
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?",(user_id,))
        return self.cursor.fetchone()
        
    
    def delete_user(self, user_id):
        """
        Delete user from database.
        """
        self.cursor.execute("DELETE FROM passwords WHERE user_id = ?",(user_id,))
        self.cursor.execute("DELETE FROM users WHERE user_id = ?",(user_id,))
        self.save_changes()


    # =========================
    # Passwords
    # =========================
    

    def add_password(self, user_id, website, username, encrypted_password, encryption_salt):
        """
        Store encrypted password in database.
        """
        info = (website ,username ,encrypted_password,encryption_salt ,user_id)
        self.cursor.execute("INSERT INTO passwords (website, account_username, encrypted_password, encryption_salt, user_id) VALUES (?,?,?,?,?)",info)
        self.save_changes()

    def get_all_passwords(self, user_id):
        """
        Return all saved passwords for a user.
        """
        self.cursor.execute("SELECT * FROM passwords WHERE user_id = ?",(user_id,))
        passws = self.cursor.fetchall()
        return passws
        
            

    def get_password_by_id(self, password_id):
        """
        Return one password entry using id.
        """
        self.cursor.execute("SELECT encrypted_password FROM passwords WHERE password_id = ?",(password_id,))
        return self.cursor.fetchone()

    def get_salt(self ,password_id):
        self.cursor.execute("SELECT encryption_salt FROM passwords WHERE password_id = ?",(password_id,))
        return self.cursor.fetchone()
    def update_password(self, password_id, new_data):
        """
        Update password entry information.
        """
        self.cursor.execute("UPDATE passwords SET encrypted_password = ? WHERE password_id = ?",(new_data,password_id))
        self.save_changes()

    def delete_password(self, password_id):
        """
        Remove password entry from database.
        """
        self.cursor.execute("DELETE FROM passwords WHERE password_id = ?",(password_id,))
        self.save_changes()

    # =========================
    # Search
    # =========================

    def search_by_website(self, user_id, website):
        """
        Search password entries by website.
        """
        self.cursor.execute("SELECT * FROM passwords WHERE user_id = ? AND website = ?",(user_id,website))
        return self.cursor.fetchall()

    def search_by_username(self, user_id, username):
        """
        Search password entries by username.
        """
        self.cursor.execute("SELECT * FROM passwords WHERE user_id = ? AND account_username = ?",(user_id,username))
        return self.cursor.fetchall()
