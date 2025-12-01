import pytest # framework de tests python
import os # module pour acceder aux variables d'environnement
from pymongo import MongoClient # module pour se connecter a MongoDB
import sys # module pour modifier le chemin d'accès a Python

sys.path.append("/app")  # On ajoute /app au chemin Python pour pouvoir importer les modules du projet

from src.import_csv_to_mongo import validate_data, create_indexes # importation des fonctions validate_data et create_indexes

# --------------------------
# Configuration MongoDB pour les tests
# --------------------------

MONGO_USER = os.getenv("MONGO_USERNAME") # récupération du nom d'utilisateur MongoDB depuis les variables d'environnement
MONGO_PWD  = os.getenv("MONGO_PASSWORD") # récupération du mot de passe MongoDB depuis les variables d'environnement

@pytest.fixture(scope="module") # scope="module" signifie que le client MongoDB est créé une fois pour tous les tests
# Une "fixture" est une fonction qui prépare à l'avance les données ou les outils nécessaires aux tests.
# Avec scope="module", cette préparation est faite une seule fois pour tout le fichier de tests.
def mongo_client():
    """Création d'un client MongoDB pour les tests"""
    # "medical_db_test" base de test pour éviter de toucher à la vraie base
    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@mongo:27017/medical_db_test?authSource=admin")
    yield client # yield permet de retourner le client MongoDB pour les tests
    # 'yield' coupe la fixture en deux : d'abord on crée le client MongoDB et on fait les tests,
    # puis, une fois tous les tests terminés, le code après le yield s'exécute pour nettoyer (supprimer la base de test).
    client.drop_database("medical_db_test")  # Supprime la base test à la fin des tests

@pytest.fixture(scope="module") # scope="module" signifie que la collection est créée une fois pour tous les tests
def collection(mongo_client): # mongo_client est la fixture qui crée le client MongoDB pour les tests
    """Collection de test"""
    db = mongo_client["medical_db_test"] # création de la base de test
    coll = db["patients_test"] # création de la collection de test
    # Nettoyer la collection au début pour partir avec une collection vide
    coll.delete_many({}) # suppression de tous les documents de la collection de test
    yield coll  # On retourne la collection pour les tests
    coll.drop()  # Nettoyage après les tests pour supprimer la collection de test et revenir à une collection vide

# --------------------------
# Test de validate_data
# --------------------------
def test_validate_data():
    csv_path = "/data/healthcare_dataset.csv"  # chemin dans le conteneur migration
    df = validate_data(csv_path)  # Appel de la fonction de validation des données 
    # assert est une fonction qui permet de vérifier une condition et si elle est fausse, le test échoue
    assert df is not None, "Le CSV n'a pas été chargé correctement" # Vérifie que le DataFrame n'est pas None donc chargé correctement sinon le message d'erreur est affiché
    assert len(df) > 0, "Le CSV est vide après validation" # Vérifie que le DataFrame n'est pas vide sinon le message d'erreur est affiché
    # Vérifie qu'il n'y a plus de doublons
    assert df.duplicated().sum() == 0, "Il reste des doublons après validate_data()" # Vérifie que le DataFrame ne contient pas de doublons sinon le message d'erreur est affiché

# --------------------------
# Test de create_indexes
# --------------------------
def test_create_indexes(collection):
    # On insère un document fictif pour s'assurer que la collection existe
    doc = {"Name": "Test Patient", "Medical Condition": "Checkup", "Doctor": "Dr Test", "Date of Admission": "2025-01-01"}
    collection.insert_one(doc) # Insertion du document fictif dans la collection
    
    # Création des index grace a la fonction create_indexes
    create_indexes(collection)

    # Vérification que les index existent grace a la fonction index_information
    indexes = collection.index_information() #exemple : {"_id_": {...},"Name_1": {...},...} donc keys() = ["_id_", "Name_1",...]
    expected_indexes = ["Name", "Medical Condition", "Doctor", "Date of Admission"] # Liste des index attendus
    for idx in expected_indexes: # Boucle sur chaque index attendu
        assert any(idx in k for k in indexes.keys()), f"Index sur {idx} manquant" # Vérifie que l'index existe sinon le message d'erreur est affiché
        # exemple : On teste si idx est contenu dans k → "Name" in "Name_1" → True
