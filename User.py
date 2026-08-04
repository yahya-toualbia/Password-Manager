# =========================
# models.py
# =========================


class User:

    def __init__(self, entry_id, username, master_password):
        """
        Create User object.
        """
        self.username = username
        self.entry_id = entry_id
        self.master_password = master_password

    def to_dict(self):
        """
        Convert user object to dictionary.
        """
        usr_info_dic = {
            "username":self.username,
            "user id" : self.entry_id,
            "password" : self.master_password,
        }
        return usr_info_dic

    def __str__(self):
        """
        Return readable user information.
        """
        return f"username -> {self.username} | user ID -> {self.entry_id} | password hash -> {self.master_password}"


class PasswordEntry:

    def __init__(self, entry_id, website, username, encrypted_password):
        """
        Create password entry object.
        """
        self.entry_id = entry_id
        self.website = website
        self.username = username
        self.encrypted_password = encrypted_password

    def to_dict(self):
        """
        Convert password entry to dictionary.
        """
        passwd_info_dic = {
            "password ID" : self.entry_id,
            "website" : self.website,
            "username" : self.username,
            "encrypted password" : self.encrypted_password
        }
        return passwd_info_dic

    def __str__(self):
        """
        Return readable password entry information.
        """
        return f"password ID -> {self.entry_id} | website -> {self.website} | username -> {self.username} | encrypted password -> {self.encrypted_password}"
    