import os
from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.host = os.environ['host']
        self.port = int(os.environ['port'])
        self.username = os.environ['user']
        self.password = os.environ['pass']
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.host, self.port, username=self.username, password=self.password)
            # self.client = MongoClient(
            #     "mongodb://" + self.username + ":" + self.password + "@" + self.host + ":" + str(self.port) + "/")
            self.db = self.client["hyperpoly"]  # Remplacez 'myFirstDatabase' par le nom de votre base de données
            print("Connexion à la base de données réussie.")
        except Exception as e:
            print("Erreur lors de la connexion à la base de données:", str(e))

    def disconnect(self):
        try:
            self.client.close()
            print("Déconnexion de la base de données réussie.")
        except Exception as e:
            print("Erreur lors de la déconnexion de la base de données:", str(e))

    def insert_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            print("Document inséré avec l'ID:", result.inserted_id)
        except Exception as e:
            print("Erreur lors de l'insertion du document:", str(e))

    def delete_document(self, collection_name, filter):
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(filter)
            if result.deleted_count == 1:
                print("Document supprimé avec succès.")
            else:
                print("Aucun document correspondant n'a été trouvé.")
        except Exception as e:
            print("Erreur lors de la suppression du document:", str(e))

    def insert_server(self, guild_id, channel_id, user, password, average):
        try:
            collection = self.db["server"]
            result = collection.insert_one(
                {
                    guild_id: guild_id,
                    channel_id: channel_id,
                    user: user,
                    password: password,
                    average: average,
                }
            )
            print("Document inséré avec l'ID:", result.inserted_id)
        except Exception as e:
            print("Erreur lors de l'insertion du document:", str(e))

    # Ajoutez d'autres méthodes pour effectuer des opérations CRUD (create, read, update, delete)

# from pymongo import MongoClient
#
# URI = "mongodb://user:pass@localhost:27017/"
# client = MongoClient(URI)
#
# dbname = client['myFirstDatabase']
#
# collection_name = dbname["user"]
#
# item_1 = {
#     "name": "emile2",
#     "nom": "dupond2",
#     "number": "RR450020FRG",
# }
#
# collection_name.insert_one(item_1)
#
# print("Connection Successful")
