import configparser
import os
import sys

helper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../helper")
sys.path.insert(1, r'' + helper_folder)

from Logger import logger
class MyCredentials:

    def __init__(self):
        """
        Initializes an instance of the MyCredentials class.
        """
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config/my_config.ini")
        self.credentials_exist()

        self.config = configparser.RawConfigParser()
        self.config.read(self.file_path)

    def credentials_exist(self):
        """
         Checks if the credentials file exists.
         """
        if (not os.path.exists(self.file_path)):
            logger.error("Credentials doesn't exist")
            exit()
            # self.create_credentials()
        else:
            logger.info("Credentials exist")

    def create_credentials(self):
        """
        Creates a new credentials file and prompts the user for username, password, and webhook URL.
        """
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
        """
        Returns the username from the credentials file.

        Returns:
        - str: The username.
        """
        return self.config.get('user', 'username')

    def get_user_password(self):
        """
        Returns the user password from the credentials file.

        Returns:
        - str: The user password.
        """
        return self.config.get('user', 'password')

    def get_webhook_url(self):
        """
        Returns the webhook URL from the credentials file.

        Returns:
        - str: The webhook URL.
        """
        return self.config.get('webhook', 'url')
