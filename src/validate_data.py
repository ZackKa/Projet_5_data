import pandas as pd  # Importation de la bibliothèque pandas pour manipuler des données tabulaires

# Charger le CSV original
# pd.read_csv lit le fichier CSV et le transforme en DataFrame pandas
# sep=";" indique que le séparateur de colonnes est le point-virgule
df = pd.read_csv("../data/healthcare_dataset.csv", sep=";")

# Affichage des noms des colonnes du DataFrame
print("\nCOLONNES")
print(df.columns)  # df.columns renvoie une liste des colonnes du CSV

# Affichage des types de données de chaque colonne
print("\nTYPES")
print(df.dtypes)  # df.dtypes indique si chaque colonne est int, float, object (texte), etc.

# Vérification des valeurs manquantes
print("\nVALEURS MANQUANTES")
print(df.isna().sum())  
# df.isna() retourne un DataFrame avec True pour les valeurs manquantes
# sum() fait le total des valeurs manquantes par colonne

# Vérification des doublons
print("\nDOUBLONS")
print(df.duplicated().sum())  
# df.duplicated() retourne True pour les lignes identiques à une précédente
# sum() donne le nombre total de doublons

# Affichage des premières lignes pour avoir un aperçu des données
print("\nAPERÇU")
print(df.head())  # df.head() montre les 5 premières lignes du DataFrame par défaut

# Affichage des statistiques descriptives
print("\nSTATISTIQUES")
print(df.describe(include='all'))  
# df.describe() donne des stats comme moyenne, min, max, quartiles pour les colonnes numériques
# include='all' inclut aussi les colonnes non numériques (texte), avec comptage, valeurs uniques, etc.
