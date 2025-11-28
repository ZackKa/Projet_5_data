from pymongo import MongoClient  # Import de MongoClient pour se connecter à MongoDB

# Connexion au serveur MongoDB local sur le port par défaut 27017
client = MongoClient("mongodb://localhost:27017/")

# Sélection de la base de données "medical_db"
db = client["medical_db"]

# Sélection de la collection "patients"
collection = db["patients"]

#           CREATE          
print("\nCREATE")
# Création d'un nouveau document représentant un patient
new_patient = {
    "Name": "John TEST",
    "Age": 45,
    "Gender": "Male",
    "Medical Condition": "Checkup",
    "Date of Admission": "2025-01-01",
    "Hospital": "Hospital Test",
    "Doctor": "Dr Test",
    "Insurance Provider": "Test Insurance",
    "Billing Amount": 0.0,
    "Room Number": "001",
    "Admission Type": "Emergency",
    "Discharge Date": "2025-01-02",
    "Medication": "Aspirin",
    "Test Results": "Normal",
}

# Insertion du document dans la collection
insert_result = collection.insert_one(new_patient)
# MongoDB crée automatiquement un _id unique pour ce document si on ne l'a pas précisé
# inserted_id permet de récupérer cet ID dans Python, crée automatiquement par MongoDB
print(f"Inserted ID : {insert_result.inserted_id}")

#           READ          
print("\nREAD")
# Recherche du premier document correspondant au filtre {"Name": "John TEST"}
patient = collection.find_one({"Name": "John TEST"})
# Affichage du document trouvé
print(patient)

#           UPDATE          
print("\nUPDATE")
# Modification d'un document existant : ici on met à jour le champ "Billing Amount"
collection.update_one(
    {"Name": "John TEST"},           # Filtre pour trouver le document
    {"$set": {"Billing Amount": 100}} # Opérateur $set pour modifier uniquement ce champ
)
# Vérification de la modification
updated = collection.find_one({"Name": "John TEST"})
print(updated)

#           DELETE          
print("\nDELETE")
# Suppression du document correspondant au filtre {"Name": "John TEST"}
collection.delete_one({"Name": "John TEST"})
# Vérification que le document a été supprimé
deleted = collection.find_one({"Name": "John TEST"})
print("After delete :", deleted) # affiche None car le document a été supprimé
