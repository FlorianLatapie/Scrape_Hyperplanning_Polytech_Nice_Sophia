import geckodriver_autoinstaller
from selenium import webdriver

# Installer automatiquement la dernière version du pilote WebDriver pour Firefox
geckodriver_autoinstaller.install()

# Afficher la version du pilote WebDriver de Firefox installée
print(webdriver.FirefoxOptions().gecko_version)
