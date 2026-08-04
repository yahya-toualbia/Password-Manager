from Auth import AuthManager
from Password import PasswordManager
from Database import DatabaseManager
from User import *
db = DatabaseManager()
auth = AuthManager(db)
password_manager = PasswordManager(auth ,db)
ask = """what do you want to do 
[1]- create_password_entry
[2]- show_all_passwords
[3]- view_password
[4]- edit_password
[5]- remove_password
[6]- search_passwords
[7]- generate_password
[8]- check_password_strength
[9]- show_info
[10]- delete_user
[11]- exit
-> """
def after_login(master_password):
        while password_manager.auth.is_authenticated():
            while True:
                try:
                    num = int(input(ask))
                    break
                except:
                    print("try again")
            if num == 1:
                website = input("name of website: ")
                account_username = input("username: ")
                password = input("password: ")
                if password_manager.create_password_entry(website ,account_username ,password ,master_password):
                    print("the password created successfully")
                else:
                    print("some thing is hapend try again later")
            elif num == 2:
                print(password_manager.show_all_passwords(master_password))
            elif num == 3:
                while True:
                    try:
                        password_id = int(input("""we need password ID
if you did not have it pass this question by type 0 and check the ID in show_all_passwords
password ID(number): """))
                        break
                    except ValueError:
                        print("you have enter a letter try again")
                if password_id == 0:
                    return False
                print(password_manager.reveal_password(password_id, master_password))
            elif num == 4:
                while True:
                    try:
                        password_id = int(input("""we need password ID
if you did not have it pass this question by type 0 and check the ID in show_all_passwords
password ID(number): """))
                        break
                    except ValueError:
                        print("you have enter a letter try again")
                if password_id == 0:
                    return False
                new_password = input("the new password: ")
                if password_manager.edit_password(password_id ,new_password ,master_password):
                    print("done")
                else:
                    print("some thing is hapend try again later")
            elif num == 5:
                while True:
                    try:
                        password_id = int(input("""we need password ID
if you did not have it pass this question by type 0 and check the ID in show_all_passwords
password ID(number): """))
                        break
                    except ValueError:
                        print("you have enter a letter try again")
                if password_id == 0:
                    return False
                confirm = input("are you sure? (y/n): ")
                if confirm.lower() == "y":
                    if password_manager.remove_password(password_id):
                        print("done")
                else:
                    print("some thing is hapend try again later")
            elif num == 6:
                website = input("name of website: ")
                print(password_manager.search_passwords(website))
            elif num == 7:
                tall = int(input("the tall of the generated password: "))
                print(password_manager.generate_password(tall))
            elif num == 8:
                password = input("enter the password: ")
                print(password_manager.check_password_strength(password))
            elif num == 9:
                current_usr = auth.current_user
                current_usr_id = auth.current_user_id
                user = User(current_usr_id,current_usr,master_password)
                print(user.to_dict())
            elif num == 10:
                current_usr_id = auth.current_user_id
                confirm = input("are you sure? (y/n): ")
                if confirm.lower() == "y":
                    db.delete_user(current_usr_id)
                    print("account deleted")
                    password_manager.auth.logout()
                    break
            elif num == 11:
                password_manager.auth.logout()
                password_manager.close()
                break

while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("> ")

    if choice == "1":
        username = input("enter your name: ")
        m_password = input("enter your master password: ")
        if password_manager.auth.register(username, m_password):
            print("the account created successfully")
            result = password_manager.auth.login(username, m_password)
            if result:
                print("login successfully")
                after_login(m_password)
                break
            elif result == False:
                print("master password is wrong try again")
            elif result == None:
                print("user not found")

        else:
            print("this username is already exestes try with other username")
    elif choice == "2":
        username = input("enter your name: ")
        m_password = input("enter your master password: ")
        result = password_manager.auth.login(username, m_password)
        if result:
            print("login successfully")
            after_login(m_password)
            break
        elif result == False:
            print("master password is wrong try again")
        elif result == None:
            print("user not found")
    elif choice == "3":
        db.close_connection()
        break