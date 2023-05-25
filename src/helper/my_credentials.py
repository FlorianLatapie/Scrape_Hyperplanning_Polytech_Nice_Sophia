import configparser
import os

import os.path
class My_credentials:

    def __init__(self):
        self.path_file = "../../config/my_config.ini"

        self.credentials_exist()

        self.config = configparser.RawConfigParser()
        self.config.read(self.path_file)

    def credentials_exist(self):
        if (not os.path.exists(self.path_file)):
            print("credentials doesn't exist")
            self.create_credentials()
        else:
            print("credentials exist")

    def create_credentials(self):
        file = open(self.path_file, "w")
        username = input("What is your username : ")
        password = input("What is your password : ")
        token = input("What is your bot token : ")
        file.writelines(
            ["[user]\n",
             "username = " + username + "\n",
             "password = " + password + "\n",
             "\n",
             "[bot]\n",
             "token = " + token + "\n"])

    def get_username(self):
        return self.config.get('user', 'username')

    def get_user_password(self):
        return self.config.get('user', 'password')

    def get_bot_token(self):
        return self.config.get('bot', 'token')