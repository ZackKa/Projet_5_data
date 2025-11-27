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
- Mise en place d’un système d’authentification sécurisé (admin / rw / read)

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
├── init/
│   └── init_users.js   (création des utilisateurs MongoDB)
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
├── .env
├── .gitignore
├── wait_for_mongo.py
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

Pour la partie 1 ,dans le fichier `import_csv_to_mongo.py`, 
- remplacer ` dataHealthcare = pd.read_csv("/data/healthcare_dataset.csv", sep=";") ` par `dataHealthcare = pd.read_csv("../data/healthcare_dataset.csv", sep=";")` 
et `client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@mongo:27017/medical_db?authSource=admin")` par `client = MongoClient("mongodb://localhost:27017/")`. 
- et supprimer `MONGO_USER = os.getenv("MONGO_USERNAME")` et `MONGO_PWD = os.getenv("MONGO_PASSWORD")`

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
mongodb://{MONGO_USER}:{MONGO_PWD}@localhost:27018/medical_db?authSource=admin
```
!!! {MONGO_USER} et {MONGO_PWD} à remplacer par l'identifiant et le mot de passe, lors de la connexion dans MongoDB compass


## 12. Conteneurisation Docker

## 12.1 docker-compose.yml

Conteneur MongoDB

Conteneur de migration automatique

Volume persistant projet_5_mongo_data

Réseau dédié

MongoDB est lancé avec un script d’initialisation :
```bash
init/init_users.js
```

MongoDB écoute sur le port 27018 pour éviter les conflits locaux.


## 12.2 Dockerfile.migration

installe Python

Installation des dépendances

Lancement automatique du script import_csv_to_mongo.py


## 12.3 Authentification & Rôles utilisateurs (MongoDB)

Trois utilisateurs sont créés automatiquement au démarrage :

Ces utilisateurs sont créés par le script :

```bash
init/init_users.js
```
   ###  1- admin_user

   - gestion des bases et des utilisateurs

   - accès total

   - rôle :

      - userAdminAnyDatabase

      - dbAdminAnyDatabase

      - readWriteAnyDatabase

   C'est le super administrateur du projet.


   ###  2- rw_user (Read & Write sur medical_db)

   - Accès lecture + écriture

   - Utilisé pour la migration et les opérations CRUD

   - Rôle :

      { role: "readWrite", db: "medical_db" }


   URI pour se connecter :
   ```bash
   mongodb://{MONGO_USER}:{MONGO_PWD}@localhost:27018/medical_db?authSource=admin
   ```
  
  ###  3- read_user (Lecture seule)

   - Consultation uniquement

   - Aucun droit d'écriture

   - Rôle :

      { role: "read", db: "medical_db" }



## 12.4 Démarrer Docker

Construire et démarrer les conteneurs depuis zéro
```bash
docker-compose up --build -d
```

Arrêter les conteneurs
```bash
docker-compose down
```

Démarrer l’infrastructure Docker quand elle est arrêtée
```bash
docker-compose up -d
```
ou utiliser l'interface docker desktop

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
docker exec -it proj5_mongo mongosh -u {MONGO_USER} -p {MONGO_PWD} --authenticationDatabase admin
```
!!! Remplacer {MONGO_USER} et {MONGO_PWD} par l'identifiant et le mot de passe



## Conclusion – Étape 2 : Migration via Docker

La deuxième étape du projet montre que la migration vers MongoDB peut être automatisée, conteneurisée et sécurisée grâce à Docker et à un système d’authentification complet.

### Conteneurisation & Automatisation

   - Migration exécutée automatiquement grâce à un conteneur dédié.

   - Attente du démarrage de MongoDB, puis import du CSV via un script Python.

   - Utilisation d’un conteneur « one-shot » qui effectue la migration puis s’arrête.

   - Procédure totalement reproductible : mêmes scripts, mêmes versions, mêmes résultats.

   - Portabilité : exécutable sur n’importe quelle machine sans configuration manuelle.

### Scalabilité & Simplicité d’usage

   - MongoDB tourne dans un conteneur isolé avec volume persistant.

   - Le système peut gérer facilement de grands volumes de données.

   - Démarrage, inspection et interaction via quelques commandes Docker.

   - Intégration simple avec MongoDB Compass pour visualiser et vérifier les données.

### Authentification & Gestion des rôles

   - Système d’authentification activé automatiquement au premier démarrage.

   - Création de plusieurs comptes selon les besoins :

      - Administrateur : gestion des bases et des utilisateurs.

      - Read/Write : utilisé pour la migration et les opérations CRUD.

      - Read-Only : dédié à la consultation et à l’analyse.

   - Séparation claire des rôles : accès complet, accès lecture/écriture, accès lecture seule.

   - Mots de passe automatiquement hachés par MongoDB, garantissant la sécurité.

   - Le conteneur de migration se connecte uniquement via l’utilisateur Read/Write, limitant les privilèges.


##   Conclusion générale

Le projet a permis de mettre en place une solution complète et robuste pour moderniser la gestion des données du client.

La première étape a fourni une base solide : migration fiable des données depuis le CSV, préparation et nettoyage, opérations CRUD et optimisation grâce aux index.

La deuxième étape a renforcé cette solution avec l’automatisation, la conteneurisation via Docker, la portabilité et la reproductibilité, tout en intégrant un système d’authentification sécurisé avec des rôles clairement définis.

Ainsi, le projet offre une infrastructure fiable, scalable, sécurisée et prête pour un déploiement cloud, répondant pleinement aux besoins du client.