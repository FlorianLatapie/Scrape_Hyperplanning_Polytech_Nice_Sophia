# Scrape Hyperplanning Polytech Nice Sophia

Ces scripts Python utilisent Selenium avec Microsoft Edge comme WebDriver.

## Fonctionnalités

![image](https://user-images.githubusercontent.com/70631622/213049214-a962caee-6548-427f-8e13-57cd612e6031.png)

### `scrape_files.py`

Télécharge tous les fichiers de la catégorie *Enseignements/Ressources pédagogiques* et les dépose dans un répertoire `downloads/` à la racine du projet.

### `scape_notes.py`

Vérifie si la moyenne de l'étudiant a changé (comparaison avec `average.txt`) et indique dans la console s'il c'est le cas.

## À voir aussi

- [Hyperplanning PNS par João Brilhante](https://github.com/JoaoBrlt/hyperplanning-pns) : Application permettant de récupérer des informations sur la disponibilité des salles de classe à Polytech Nice Sophia en utilisant le système Hyperplanning en utilisant l'API de calendrier (http://sco.polytech.unice.fr/1/Telechargements/ical/schedule.ics?version=2020.0.6.0&idICal={identifier}) et analysant les fichiers `.ical`.
