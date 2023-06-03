import configparser
import os
import sys

helper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../helper")
sys.path.insert(1, r'' + helper_folder)

from Logger import logger
class MyCredentials:

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config/my_config.ini")
        self.credentials_exist()

        self.config = configparser.RawConfigParser()
        self.config.read(self.file_path)

    def credentials_exist(self):
        if (not os.path.exists(self.file_path)):
            logger.info("Credentials doesn't exist")
            exit()
            # self.create_credentials()
        else:
            logger.info("Credentials exist")

    def create_credentials(self):
        file = open(self.file_path, "w")
        username = input("What is your username : ")
        password = input("What is your password : ")
        url = input("What is your webhook url : ")
        file.writelines(
            ["[user]\n",
             "username = " + username + "\n",
             "password = " + password + "\n",
             "\n",
             "[webhook]\n",
             "url = " + url + "\n"])

    def get_username(self):
        return self.config.get('user', 'username')

    def get_user_password(self):
        return self.config.get('user', 'password')

    def get_webhook_url(self):
        return self.config.get('webhook', 'url')
