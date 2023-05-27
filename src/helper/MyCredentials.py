import configparser
import os

import os.path
class MyCredentials:

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config/my_config.ini")

        self.credentials_exist()

        self.config = configparser.RawConfigParser()
        self.config.read(self.file_path)

    def credentials_exist(self):
        if (not os.path.exists(self.file_path)):
            print("credentials doesn't exist")
            self.create_credentials()
        else:
            print("credentials exist")

    def create_credentials(self):
        file = open(self.file_path, "w")
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
