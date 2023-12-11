import os
import time
import argparse


import credentials_handler
from webdriver_handler import WebDriverFactory


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# # Consts
link = "http://sco.polytech.unice.fr/1/etudiant"
verbose = True

# # Prepare
if verbose:
    start_time = time.time()

credentials = credentials_handler.return_login_password()

arg_parser = argparse.ArgumentParser(prog="scrape_files.py")
arg_parser.add_argument("--webdriver", "-wd", type=str, default=WebDriverFactory.DEFAULT, help="webdriver to use")
arg_parser.add_argument("--no-headless", action='store_false', default=True, help="display browser or not")
args = arg_parser.parse_args()

driver = WebDriverFactory.get(args.webdriver).get_driver(headless=args.no_headless)

# ## Start browser
if verbose:
    print("Browser started ...")

driver.get(link)

# ### Login page
driver.find_element(By.ID, 'username').send_keys(credentials[0])
driver.find_element(By.ID, 'password').send_keys(credentials[1])
driver.find_element(By.NAME, 'submit').click()

# ### Home page
dernieres_notes = "//header[@title='Les 10 dernières notes']"
WebDriverWait(driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, dernieres_notes))
driver.find_element(By.XPATH, dernieres_notes).click()

# ### Dernières notes page
WebDriverWait(driver, 10).until(lambda driver_: driver_.find_elements(By.CLASS_NAME, "ie-titre-gros"))

# #### find average written in the last line
ie_titre_gros_html_tags = driver.find_elements(By.CLASS_NAME, "ie-titre-gros")
nb_of_ie_titre_gros = len(ie_titre_gros_html_tags)
average = float(ie_titre_gros_html_tags[nb_of_ie_titre_gros-1].get_attribute('innerHTML').replace(',', '.'))
print("found average :", average)

# #### find every single note

notes = [note_devoir for note_devoir in driver.find_elements(By.CLASS_NAME, "note-devoir")]

for note in notes:
    print("note :", note.get_attribute('innerHTML'))


"""
liste_celluleGrid = driver.find_elements(By.CLASS_NAME, "liste_celluleGrid")
nb_of_liste_celluleGrid = len(liste_celluleGrid)
print("nb_of_liste_celluleGrid :", nb_of_liste_celluleGrid)

for celluleGrid in liste_celluleGrid:
    # print first children of the first children of celluleGrid
    celluleGrid_children = celluleGrid\
        .find_elements(By.XPATH, "./*")[0] \
        .find_elements(By.XPATH, "./*")[0] \
        .find_elements(By.XPATH, "./*")[0]

    zone_gauche = celluleGrid_children.find_elements(By.XPATH, "./*")[0]
    zone_centrale = celluleGrid_children.find_elements(By.XPATH, "./*")[1]

    # if zone_gauche has a <span> child, its a category else if it has a <time> child, its a note
    if zone_gauche.find_elements(By.XPATH, "./*")[0].tag_name == "span":
        # its a category
        category = "category :", zone_centrale\
            .find_elements(By.XPATH, "./*")[0]\
            .find_elements(By.XPATH, "./*")[0]\
            .find_elements(By.XPATH, "./*")[0]\
            .find_elements(By.XPATH, "./*")[0]\
            .get_attribute('innerHTML').replace("&amp;", "&")

        print("category :", zone_centrale.find_elements(By.XPATH, "./*")[0].find_elements(By.XPATH, "./*")[0].find_elements(By.XPATH, "./*")[0].find_elements(By.XPATH, "./*")[0].get_attribute('innerHTML').replace("&amp;", "&"))
    elif zone_gauche.find_elements(By.XPATH, "./*")[0].tag_name == "time":
        # its a note
        date = zone_gauche.find_elements(By.XPATH, "./*")[0].get_attribute('innerHTML')
        nom_note = zone_centrale\
            .find_elements(By.XPATH, "./*")[0] \
            .find_elements(By.XPATH, "./*")[0] \
            .find_elements(By.XPATH, "./*")[-1] \
            .find_elements(By.XPATH, "./*")[0] \
            .get_attribute('innerHTML')
        print("\tnote :", nom_note, " le", date)
    else:
        print("error")
"""
print("waiting ...")

while True:
    time.sleep(1)

if not os.path.exists("average.txt"):
    average_file = open("average.txt", "w")
    average_file.write(str(average))
    average_file.close()

with open("average.txt", "r") as average_file:
    average_file_content = average_file.read()
    print("average_file_content :", average_file_content)
    # compare average with average_file_content
    if average != float(average_file_content):
        print("\033[92m" + "New average detected : " + str(average) + "\033[0m")
        # write the new average in average.txt
        average_file = open("average.txt", "w")
        average_file.write(str(average))
        average_file.close()
    else:
        print("\033[93m" + "No new average detected : " + str(average) + "\033[0m")

# ## Close browser

driver.quit()

if verbose:
    print("Browser closed ...")
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} s")
