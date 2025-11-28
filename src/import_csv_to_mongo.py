import pandas as pd
import os
from pymongo import MongoClient

# ============================================================
# 1. VALIDATION DES DONNÉES (ex-validate_data.py)
# ============================================================

def validate_data(csv_path):
    """
    Valide le CSV avant migration :
    - affichage colonnes
    - types
    - valeurs manquantes
    - doublons
    - aperçu
    - statistiques
    
    Retourne le DataFrame si tout est OK.
    """

    print("\n===== VALIDATION DES DONNÉES =====")

    # Chargement du CSV
    try:
        # pd.read_csv lit le fichier CSV et le transforme en DataFrame pandas
        # sep=";" indique que le séparateur de colonnes est le point-virgule
        df = pd.read_csv(csv_path, sep=";")
        print("CSV chargé avec succès.")
    except Exception as e:
        # Gestion des erreurs si le CSV est introuvable ou mal formaté
        print(f"Erreur lors du chargement du CSV : {e}") # affiche l'erreur
        return None # retourne None si l'erreur est survenue

    # Affichage colonnes
    print("\nCOLONNES :")
    print(df.columns)

    # Types
    print("\nTYPES :")
    print(df.dtypes)

    # Valeurs manquantes
    print("\nVALEURS MANQUANTES :")
    print(df.isna().sum()) # affiche le nombre de valeurs manquantes par colonne

    # Doublons
    duplicated_rows = df[df.duplicated()]  # sélectionne les lignes dupliquées en retournant en retournant true pour les lignes dupliquées
    nb_doublons = duplicated_rows.shape[0] # renvoie le nombre de lignes dupliquées grace a shape[0]
    print("\nDOUBLONS :")
    print(nb_doublons)

    if nb_doublons > 0:
        print("Attention : des doublons sont présents. Voici les lignes dupliquées :")
        print(duplicated_rows)  # Affiche les lignes complètes
        print("\nCes doublons seront supprimés.")
        df = df.drop_duplicates() # supprime les lignes dupliquées


    # Aperçu
    print("\nAPERÇU :")
    print(df.head()) # affiche les 5 premières lignes du DataFrame

    # Statistiques
    print("\nSTATISTIQUES :")
    print(df.describe(include='all')) # affiche les statistiques descriptives de toutes les colonnes

    print("\nValidation terminée.\n")
    return df # retourne le DataFrame si tout est OK



# ============================================================
# 2. CRÉATION DES INDEX (ex-create_indexes.py)
# ============================================================

def create_indexes(collection):
    """
    Crée automatiquement les index nécessaires sur la collection.
    """
    print("\n===== CRÉATION DES INDEX =====")

    # Liste des champs sur lesquels on souhaite créer des index
    indexes = [
        "Name",
        "Medical Condition",
        "Doctor",
        "Date of Admission"
    ]

    # Boucle sur chaque champ de la liste "indexes"
    for element in indexes:
        try:
            collection.create_index(element) # create_index est une méthode fournie par PyMongo qui demande à MongoDB de créer un index sur le champ spécifié
            print(f" Index créé sur : {element}")
        except Exception as e:
            print(f" Erreur lors de la création de l'index sur {element} : {e}")

    print("Indexation terminée.\n")



# ============================================================
# 3. MIGRATION DES DONNÉES
# ============================================================

def migrate_data(df, collection): 
    """
    Insère les données validées dans MongoDB.
    """
    print("\n===== MIGRATION DES DONNÉES =====")

    # converti le DataFrame en liste de dictionnaires grace a to_dict(orient="records")
    records = df.to_dict(orient="records")

    # insert_many est une méthode fournie par PyMongo qui demande à MongoDB de insérer les documents dans la collection
    result = collection.insert_many(records)
    # affiche le nombre de documents insérés grace a len(result.inserted_ids)
    print(f"{len(result.inserted_ids)} documents insérés dans MongoDB.\n") #inserted_ids crée des id unique pour chaque document inséré
    



# ============================================================
# 4. PIPELINE PRINCIPAL
# ============================================================

def main():
    print("===== DÉBUT DU PIPELINE DE MIGRATION =====\n")

    CSV_PATH = "/data/healthcare_dataset.csv" # chemin du fichier CSV

    # --- Étape 1 : Validation ---
    df = validate_data(CSV_PATH) # appelle la fonction validate_data avec le chemin du fichier CSV

    if df is None:
        print("Erreur : Validation impossible, arrêt du programme.")
        return

    # --- Étape 2 : Connexion MongoDB ---
    print("Connexion à MongoDB...")

    MONGO_USER = os.getenv("MONGO_USERNAME") # récupère le nom d'utilisateur MongoDB depuis les variables d'environnement
    MONGO_PWD = os.getenv("MONGO_PASSWORD") # récupère le mot de passe MongoDB depuis les variables d'environnement

    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@mongo:27017/medical_db?authSource=admin") # crée une connexion à MongoDB

    db = client["medical_db"] # sélectionne la base de données "medical_db"
    collection = db["patients"] # sélectionne la collection "patients"

    print("Connexion MongoDB établie.\n")

    # --- Étape 3 : Migration ---
    migrate_data(df, collection) # appelle la fonction migrate_data avec le DataFrame et la collection

    # --- Étape 4 : Création des index ---
    create_indexes(collection) # appelle la fonction create_indexes avec la collection

    print("===== MIGRATION TERMINÉE AVEC SUCCÈS =====")


# Lancement du script
if __name__ == "__main__": # si le script est exécuté directement et pas importé comme un module, __name__ vaut "__main__"
    main()