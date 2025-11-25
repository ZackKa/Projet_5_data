# README – Projet 5 Data Engineer : Migration des données médicales vers MongoDB

## 1. Contexte du projet

Ce projet a été réalisé dans le cadre d’une mission interne pour DataSoluTech, visant à accompagner un client dans la modernisation de son architecture data.
L’objectif est d’aider un client à améliorer la scalabilité de son système de gestion de données médicales en migrant son dataset vers une base de données MongoDB, plus adaptée pour des volumes importants.

1- Migrer le dataset du client vers une base de données MongoDB locale
ça inclut :  
- L'analyse et la validation du dataset  
- La migration vers MongoDB, adaptée aux gros volumes
- La mise en place d’opérations CRUD  
- La création d’index pour optimiser les performances 

2- Automatiser la migration des données grâce à des scripts Python pour la validation, l’insertion et la manipulation, tout en conteneurisant MongoDB et les scripts via Docker afin de disposer d’une infrastructure portable, reproductible et scalable, facilitant les futurs déploiements sur le cloud.
ça inclut : 
- automatisé cette migration via un script Python,
- conteneurisé MongoDB et le script via Docker,
- mis en place une structure reproductible, portable et facilement déployable

Le projet se compose donc de deux étapes principales :

Étape 1 : Migration classique et manipulation locale via MongoDB et CSV.
Étape 2 : Migration automatisée via Docker avec conteneurs pour MongoDB et scripts de migration.

## 2. Structure du projet

Etape 1 :
```
Projet_5_data/
│
├── data/
│   └── healthcare_dataset.csv
│
├── src/
│   ├── import_csv_to_mongo.py
│   ├── validate_data.py
│   ├── crud_examples.py
│   └── create_indexes.py
│
│
├── requirements.txt
└── README.md
```
Etapes 2 :
```
Projet_5_data/
│
├── data/
│   └── healthcare_dataset.csv
│
├── src/
│   ├── import_csv_to_mongo.py
│   ├── validate_data.py
│   ├── crud_examples.py
│   └── create_indexes.py
│
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.migration
├── .dockerignore
└── README.md
```

## Étape 1 – Migration classique et manipulation locale

## 3. Pré-requis techniques

- **Python 3.13.5**  
- **MongoDB Compass**  

MongoDB local tourne sur :  

mongodb://localhost:27017/


### Bibliothèques Python nécessaires
(installées via `requirements.txt`)  
- pandas  
- pymongo  

Pour installer les dépendances :  
```bash
pip install -r requirements.txt
```


## 4. Description du dataset

Le fichier `healthcare_dataset.csv` contient 55 500 lignes de données médicales anonymisées.

### Colonnes principales
- Name
- Age
- Gender
- Blood Type
- Medical Condition
- Date of Admission
- Doctor
- Hospital
- Insurance Provider
- Billing Amount
- Room Number
- Admission Type
- Discharge Date
- Medication
- Test Results

Le séparateur utilisé dans le CSV est `;`.

---

## 5. Validation des données (`validate_data.py`)

Avant toute migration, j’ai effectué :
- Vérification des colonnes
- Vérification des types
- Recherche de valeurs manquantes
- Recherche de doublons
- Statistiques globales

Ce script permet de s’assurer que les données sont propres avant de les insérer dans MongoDB.

### Lancer la validation
```bash
python src/validate_data.py
```


## 6. Migration dans MongoDB (`import_csv_to_mongo.py`)

Pour la partie 1 , remplacer ` dataHealthcare = pd.read_csv("/data/healthcare_dataset.csv", sep=";") ` par `dataHealthcare = pd.read_csv("../data/healthcare_dataset.csv", sep=";")` et `client = MongoClient("mongodb://mongo:27017/")` par `client = MongoClient("mongodb://localhost:27017/")` dans le fichier `import_csv_to_mongo.py`

Base de données : ensemble logique des collections
Collection : équivalent d’une table, mais sans schéma strict
Document : unité de données au format JSON/BSON

Ce script :  
- lit le CSV    
- transforme chaque ligne en document JSON  
- insère le tout dans MongoDB dans :  
  - Base : `medical_db`  
  - Collection : `patients`  

### Lancer la migration
```bash
python src/import_csv_to_mongo.py
```

Après exécution, MongoDB Compass montre bien 55 500 documents insérés.

## 7. Les Données

7.1. Schéma de la base de données

MongoDB étant un système NoSQL orienté documents, le schéma n’est pas imposé comme dans une base relationnelle.
Cependant, pour faciliter la compréhension et la maintenance, voici le schéma logique utilisé dans ce projet.

```
medical_db
│
└── patients (55 500 documents)
    │
    ├── _id : ObjectId
    ├── Name : String
    ├── Age : Int32
    ├── Gender : String
    ├── Blood Type : String
    ├── Medical Condition : String
    ├── Date of Admission : String
    ├── Doctor : String
    ├── Hospital : String
    ├── Insurance Provider : String
    ├── Billing Amount : Double
    ├── Room Number : Int32
    ├── Admission Type : String
    ├── Discharge Date : String
    ├── Medication : String
    └── Test Results : String

Indexes:
  - Name (1)
  - Medical Condition (1)
  - Doctor (1)
  - Date of Admission (1)
```

## 7.2 Modèle de données dans MongoDB

MongoDB est un système NoSQL orienté documents.

- **Base** : `medical_db`  
- **Collection** : `patients`  

### Exemple de document
```json
{
  "_id": ObjectId("..."),
  "Name": "Bobby Jackson",
  "Age": 30,
  "Gender": "Male",
  "Blood Type": "B-",
  "Medical Condition": "Cancer",
  "Date of Admission": "2024-01-31",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.28,
  "Room Number": 328,
  "Admission Type": "Urgent",
  "Discharge Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
```

### Type dans MongoDB

- **Age** → Int32  
- **Billing Amount** → Double  
- **Room Number** → Int32  
- **Dates** → String telles qu’elles apparaissent dans le CSV
- Tout le reste → String  

---

## 8. Opérations CRUD (`crud_examples.py`)

Le script contient 4 actions :  

- **CREATE** : Ajouter un patient  
- **READ** : Lire les patients par nom ou condition médicale  
- **UPDATE** : Modifier un champ (ex : Room Number)  
- **DELETE** : Supprimer un document  

### Lancer le script
```bash
python src/crud_examples.py
```

## 9. Indexation des données (`create_indexes.py`)

Pour améliorer les performances de recherche, plusieurs index ont été ajoutés.

### Pourquoi ces index ?

1. **Name**  
   - Utilisé très souvent en recherche  
   - Améliore la vitesse lors des recherches textuelles  

2. **Medical Condition**  
   - Idéal pour filtrer les patients par pathologie  
   - Très utile pour les statistiques ou dashboards  

3. **Doctor**  
   - Permet d’interroger les patients suivis par un médecin  

4. **Date of Admission**  
   - Essentiel pour l'analyse chronologique  
   - Accélère fortement les requêtes par période (semaine, mois, année)  

#### Pourquoi pas d'autres colonnes ?

- **Blood Type** : faible cardinalité (8 valeurs seulement) → index inutile  
- **Gender** : seulement 2 valeurs → index inutile  

### Lancer les index
```bash
python src/create_indexes.py
```

## 10. requirements.txt

Voici les dépendances du projet :

```text
pandas==2.2.3
pymongo==4.15.4
```

## Conclusion Étape 1

Cette première étape fournit au client une base solide pour moderniser la gestion de ses données, en assurant une migration fiable, contrôlée et extensible vers un système NoSQL.
Les travaux réalisés ont permis de : 
- mettre en place une base de données NoSQL adaptée au volume des données du client,
- utiliser MongoDB via des scripts Python pour charger et manipuler les données,
- la migration complète à partir du fichier CSV fourni,
- vérifier, nettoyer et préparer les données avant leur insertion,
- réaliser des opérations CRUD simples sur la base,
- améliorer la vitesse de recherche en ajoutant des index adaptés.

## Étape 2 – Migration automatisée via Docker

## 11. Pré-requis Docker

Docker Desktop

MongoDB tourne dans Docker sur :
```text
mongodb://localhost:27018
```

## 12. Conteneurisation Docker

## 12.1 docker-compose.yml

Conteneur MongoDB

Conteneur de migration automatique

Volume persistant

Réseau dédié

MongoDB écoute sur le port 27018 pour éviter les conflits locaux.

## 12.2 Dockerfile.migration

installe Python

Installation des dépendances

Lancement automatique du script import_csv_to_mongo.py

## 12.3 Démarrer Docker

Construire et démarrer les conteneurs depuis zéro
```bash
docker-compose up --build -d
```

Arrêter les conteneurs
```bash
docker-compose down
```

Démarrer l’infrastructure Docker
```bash
docker-compose up -d
```

## 12.4 Commandes Docker utiles

Vérifier que les conteneurs tournent
```bash
docker ps -a
```

Recréer depuis zéro :
```bash
docker-compose down -v
docker-compose up --build -d
```

Voir les volumes :
```bash
docker volume ls
```

Inspecter un volume en particulier :
```bash
docker volume inspect projet_5_mongo_data
```

Entrer dans MongoDB via Docker :
```bash
docker exec -it proj5_mongo mongosh
```

## Conclusion – Étape 2 : Migration via Docker

La deuxième étape du projet démontre que la migration vers MongoDB peut être automatisée et conteneurisée, offrant plusieurs avantages :

- Portabilité : l’infrastructure Docker permet de lancer MongoDB et les scripts de migration sur n’importe quelle machine sans configuration complexe.

- Reproductibilité : la même procédure Docker garantit que la base de données et la migration se comportent de manière identique sur différents environnements.

- Scalabilité : MongoDB tourne dans un conteneur dédié, avec volume persistant pour gérer de grands volumes de données.

- Simplicité d’usage : un utilisateur peut construire, démarrer, inspecter et interagir avec la base MongoDB grâce à quelques commandes Docker.

- Intégration avec MongoDB Compass : la base peut être facilement explorée et vérifiée via l’interface graphique.

Cette étape montre ainsi comment transformer une migration locale en processus automatisé, fiable et prêt pour le déploiement cloud.