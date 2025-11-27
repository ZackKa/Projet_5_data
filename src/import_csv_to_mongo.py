import pandas as pd
import os
from pymongo import MongoClient

# 1. Charger le CSV (séparateur = ;)
# pd.read_csv lit le fichier CSV et le transforme en DataFrame pandas
# sep=";" indique que le séparateur de colonnes est le point-virgule
dataHealthcare = pd.read_csv("/data/healthcare_dataset.csv", sep=";")

# 2. Connexion à MongoDB local
MONGO_USER = os.getenv("MONGO_USERNAME") # récupère l'utilisateur RW depuis l'environnement
MONGO_PWD = os.getenv("MONGO_PASSWORD") # récupère le mot de passe RW depuis l'environnement

# MongoClient se connecte au serveur MongoDB sur mongo:27017
# authSource=admin indique que l'authentification se fait sur la base admin et necessaire pour l'authentification MongoDB
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@mongo:27017/medical_db?authSource=admin")# URI MongoDB à utiliser
db = client["medical_db"]           # sélectionne ou crée la base de données 'medical_db'
collection = db["patients"]         # sélectionne ou crée la collection 'patients'

# 3. Conversion DataFrame → dictionnaires Python
# to_dict(orient="records") transforme chaque ligne du DataFrame en dictionnaire
# Exemple : {"id": 1, "nom": "Alice", "age": 34, "maladie": "Diabète"}
records = dataHealthcare.to_dict(orient="records")

# 4. Insertion dans MongoDB
# insert_many insère tous les dictionnaires dans la collection MongoDB
result = collection.insert_many(records)

# 5. Affichage du résultat
# result.inserted_ids contient la liste des identifiants (_id) générés pour chaque document
# len(result.inserted_ids) donne le nombre total de documents insérés et f pour indiquer que c'est un string
print(f"{len(result.inserted_ids)} documents insérés dans MongoDB.")
