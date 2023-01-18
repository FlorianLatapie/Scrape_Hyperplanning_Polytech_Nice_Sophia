import os

def return_login_password():
    if not os.path.exists("credentials.txt"):
        print("credentials.txt not found\nPlease enter login and password in the following format:\nlogin\npassword")
        exit(1)
    with open("credentials.txt", "r") as f:
        login = f.readline().strip()
        password = f.readline().strip()
    return login, password