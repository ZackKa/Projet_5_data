import pytest
import os
from pymongo import MongoClient
import sys

sys.path.append("/app")  # ajoute /app au chemin Python

from src.import_csv_to_mongo import validate_data, create_indexes

# --------------------------
# Configuration MongoDB pour les tests
# --------------------------

MONGO_USER = os.getenv("MONGO_USERNAME")
MONGO_PWD  = os.getenv("MONGO_PASSWORD")

@pytest.fixture(scope="module") # scope="module" signifie que le client MongoDB est créé une fois pour tous les tests
def mongo_client():
    """Création d'un client MongoDB pour les tests"""
    # "medical_db_test" base de test pour éviter de toucher à la vraie base
    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@mongo:27017/medical_db_test?authSource=admin")
    yield client # yield permet de retourner le client MongoDB pour les tests
    client.drop_database("medical_db_test")  # Supprime la base test à la fin des tests

@pytest.fixture(scope="module")
def collection(mongo_client):
    """Collection de test"""
    db = mongo_client["medical_db_test"]
    coll = db["patients_test"]
    # Nettoyer la collection au début
    coll.delete_many({})
    yield coll
    coll.drop()  # Nettoyage après les tests

# --------------------------
# Test de validate_data
# --------------------------
def test_validate_data():
    csv_path = "/data/healthcare_dataset.csv"  # chemin dans le conteneur migration
    df = validate_data(csv_path)
    assert df is not None, "Le CSV n'a pas été chargé correctement"
    assert len(df) > 0, "Le CSV est vide après validation"
    # Vérifie qu'il n'y a plus de doublons
    assert df.duplicated().sum() == 0, "Il reste des doublons après validate_data()"

# --------------------------
# Test de create_indexes
# --------------------------
def test_create_indexes(collection):
    # On insère un document fictif pour tester les index
    doc = {"Name": "Test Patient", "Medical Condition": "Checkup", "Doctor": "Dr Test", "Date of Admission": "2025-01-01"}
    collection.insert_one(doc)
    
    # Création des index
    create_indexes(collection)

    # Vérification que les index existent
    indexes = collection.index_information()
    expected_indexes = ["Name", "Medical Condition", "Doctor", "Date of Admission"]
    for idx in expected_indexes:
        assert any(idx in k for k in indexes.keys()), f"Index sur {idx} manquant"
