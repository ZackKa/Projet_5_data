from pymongo import MongoClient  # Import de MongoClient pour se connecter à MongoDB

# Connexion au serveur MongoDB local sur le port par défaut 27017
client = MongoClient("mongodb://localhost:27017/")

# Sélection de la base de données "medical_db"
db = client["medical_db"]

# Sélection de la collection "patients"
collection = db["patients"]

#                   LISTE DES INDEX 
# Liste des champs sur lesquels on souhaite créer des index
# Les index permettent d'accélérer les recherches sur ces champs
indexes = [
    "Name",
    "Medical Condition",
    "Doctor",
    "Date of Admission"
]

#                   CRÉATION DES INDEX 
# Boucle sur chaque champ de la liste "indexes"
for element in indexes: 
    # create_index est une méthode fournie par PyMongo qui demande à MongoDB de créer un index sur le champ spécifié
    collection.create_index(element)  
    # Affichage d'un message pour confirmer la création de l'index
    print(f"Index créé sur : {element}")
