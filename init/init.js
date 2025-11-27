// Script exécuté automatiquement au 1er démarrage du conteneur
// Objectif : créer les utilisateurs MongoDB

// Chargement des variables d'environnement envoyées par Docker
const rootUser = process.env.MONGO_INITDB_ROOT_USERNAME;
const rootPwd = process.env.MONGO_INITDB_ROOT_PASSWORD;

// Récupération des credentials des roles
const adminUser = process.env.MONGO_USER_ADMIN;
const adminPwd = process.env.MONGO_USER_ADMIN_PWD;

const rwUser = process.env.MONGO_USER_RW;
const rwPwd = process.env.MONGO_USER_RW_PWD;

const readUser = process.env.MONGO_USER_READ;
const readPwd = process.env.MONGO_USER_READ_PWD;

// Connexion en root à la base admin (nécessaire pour créer les comptes)
db = connect("mongodb://localhost:27017/admin", rootUser, rootPwd);

// 1) Utilisateur ADMIN : gestion complète des bases + utilisateurs
// Les "roles" sont prédéfinis par MongoDB et donnent des permissions sur une base ou globalement.

db.createUser({
  user: adminUser,
  pwd: adminPwd,
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" }, // permet de créer et gérer d'autres utilisateurs
    { role: "dbAdminAnyDatabase", db: "admin" }, // permet de créer et gérer des bases de données
    { role: "readWriteAnyDatabase", db: "admin" } // permet de lire et écrire dans toutes les bases de données
  ]
});

// 2) Utilisateur READ-WRITE : accès lecture/écriture pour l'application
db.createUser({
  user: rwUser,
  pwd: rwPwd,
  roles: [
    { role: "readWrite", db: "medical_db" } // permet de lire et écrire dans la base de données medical_db
  ]
});

// 3) Utilisateur READ : accès lecture seule pour les requêtes d'analyse
db.createUser({
  user: readUser,
  pwd: readPwd,
  roles: [
    { role: "read", db: "medical_db" } // permet de lire la base de données medical_db
  ]
});

print("Users successfully created !"); // Affiche un message via le moteur JavaScript interne de MongoDB (Mongo Shell, pas Node.js)