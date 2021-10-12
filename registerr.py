import os
import platform
import sys
import mysql.connector

def clear_everything():
    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        print("Sorry we do not now this system ")

def error():
    clear_everything()
    print("Error please try again\n")

my_db = mysql.connector.connect(
    host="localhost",
    user="abbos",
    password="12345678",
    database="dang"
)
my_cursor = my_db.cursor()
my_cursor.execute("create table if not exists register"
                  "(id int(6) unsigned auto_increment primary key, "
                  "name varchar(20), "
                  "surname varchar(20), "
                  "age int(3), "
                  "login varchar(20),"
                  " password varchar(20))")
my_db.commit()

class Register:
    def __init__(self):
        self.data = None
        self.count = 0
        self.manu()


    def sig_in(self):
        name  = self.name_surname("name")
        clear_everything()
        surname = self.name_surname("surname")
        clear_everything()
        age = self.age()
        clear_everything()
        login = self.chek_login()
        clear_everything()
        password = self.password()
        clear_everything()
        self.write_to_dabase(name,surname,age,login,password)

    def log_in(self):
        login = input("Please enter login:\n").strip().lower()
        if login:
            my_cursor.execute(f"select * from register where login='{login}'")
            result = my_cursor.fetchall()
            if result:
                clear_everything()
                while 1:
                    self.data = result
                    current_password = result[0][5]
                    password = input("Please enter your password:\n").strip()
                    if current_password == password:
                        clear_everything()
                        print("Welcome")
                        self.manu_in()
                    else:
                        error()
                        self.count += 1
                        if self.count == 4:
                            error()
                            print("You entered a lot of wrong password\n")
                            self.count = 0
                            self.log_in()
            else:
                error()
                self.log_in()
        else:
            error()
            self.log_in()



    def manu_in(self):
        answer = input("""
What do you want?
Please choose one of them
        Update login    [1]
        Update password [2]
        Log out         [3]
        Delte account   [4]
:""")
        self.choosed_in(answer)


    def choosed_in(self,chose):
        if chose == "1":
            clear_everything()
            self.update_login()
        elif chose == "2":
            clear_everything()
            self.update_password()
        elif chose == "3":
            clear_everything()
            self.log_out()
        elif chose == "4":
            clear_everything()
            self.delete_account()
        else:
            error()
            self.manu_in()

    def update_login(self):
        clear_everything()
        login = self.chek_login()
        my_cursor.execute(f"update register set login='{login}' where login='{self.data[0][4]}'")
        my_db.commit()
        clear_everything()
        print(f"Your login changed to {login}")
        self.manu_in()





    def update_password(self):
        clear_everything()
        passwordd = self.password()
        my_cursor.execute(f"update register set password='{passwordd}' where login='{self.data[0][4]}'")

        my_db.commit()
        clear_everything()
        print(f"Your password changed to {passwordd}")
        self.manu_in()

    def log_out(self):
        clear_everything()
        self.manu()

    def delete_account(self):
        sure = input("""You sure?
        Yes [1]
        No  [2]
:""")
        if sure == '1':
            my_cursor.execute(f"delete from register where login='{self.data[0][4]}'")
            my_db.commit()
            clear_everything()
            print("Your account deleted!")
            self.manu()
        elif sure == '2':
            clear_everything()
            self.manu_in()
        else:
            error()
            self.delete_account()












    # _______________________________For register____________________________________
    def manu(self):
        answer = input("""
What do you want?
Please choose one of them

        Sign in [1]
        Log in  [2]
        Exit    [3]
:""")
        self.choosed(answer)

    def choosed(self, chose):
        if chose == '1':
            clear_everything()
            self.sig_in()
        elif chose == '2':
            clear_everything()
            self.log_in()
        elif chose == '3':
            clear_everything()
            print("Bye ;)")
            exit()
        else:
            error()
            self.manu()

    def name_surname(self, name_surname):
        name = input(f"Please enter your {name_surname}:\n").capitalize().strip()
        if name.isalpha():
            return name
        else:
            error()
            self.name_surname(name_surname)

    def chek_login(self):
        login = input("Please enter new login:\n").strip().lower()
        if not login:
            error()
            self.chek_login()
        else:
            my_cursor.execute(f"select * from register where login='{login}'")
            result = my_cursor.fetchall()
            if not result:
                return login
            else:
                error()
                self.chek_login()

    def age(self):
        age = input("Please enter your age:\n").strip()
        if age:
            if age.isnumeric():
                return age
            else:
                error()
                self.age()
        else:
            error()
            self.age()

    def password(self):
        password = input("Please enter your new password:\n").strip()
        if password:
            password1 = input("Confirm password:\n").strip()
            if password1 == password:
                print(password)
                return password
            else:
                error()
                self.password()
        else:
            error()
            self.password()

    def write_to_dabase(self, name,surname,age,login,password):
        my_cursor.execute(f"insert into register"
                          f"(name,surname,age,login,password)"
                          f" values ('{name}','{surname}','{age}','{login}','{password}')")
        my_db.commit()


#   ________________________________________________________________________________________

#   ________________________________Other_______________________________________________________




register = Register()

