# On importe des modules Python standards pour utiliser des fonctions déjà écrites dans Python.
# Ces imports nous permettent de ne pas réinventer la roue.
import socket  # Pour créer une connexion réseau (TCP/IP) vers un serveur
import time    # Pour mesurer le temps et faire des pauses (sleep)
import argparse  # Pour lire les arguments passés au script depuis la ligne de commande
import sys      # Pour pouvoir quitter le script avec un code de retour (0 = succès, 1 = erreur)


# On définit notre propre fonction "wait". Elle est "créée au-dessus" du code principal.
# Cette fonction essaie de se connecter à un serveur sur un port donné et attend jusqu'à ce qu'il soit prêt.
def wait(host, port, timeout=60):
    # On enregistre le moment où on commence à attendre
    start = time.time()
    
    # Tant que le temps écoulé depuis le début est inférieur au timeout
    while time.time() - start < timeout:
        try:
            # On tente de créer une connexion TCP au serveur (host:port) avec un timeout de 3 secondes
            with socket.create_connection((host, port), timeout=3):
                # Si la connexion réussit, on affiche un message et retourne 0 (succès)
                print(f"Connected to {host}:{port}")
                return 0
        except Exception:
            # Si la connexion échoue (serveur non prêt), on affiche un message et on attend 2 secondes
            print(f"Waiting for {host}:{port} ...")
            time.sleep(2)
    
    # Si le timeout est dépassé et que le serveur n'est toujours pas prêt
    print("Timeout waiting for service.")
    return 1  # Retourne 1 = erreur


# Cette partie s'exécute uniquement si le script est lancé directement (pas importé comme module)
# Ce pattern permet d'utiliser le fichier à la fois comme script et comme module importable,
# de garder un code propre et réutilisable, et d'éviter que le code principal ne s'exécute
# automatiquement lors d'un import. C'est une pratique standard et reconnue en Python.
if __name__ == "__main__":
    # __name__ est une variable spéciale, créée automatiquement par Python dans chaque fichier. 
    # Si le fichier est exécuté directement (avec python wait_for_mongo.py), __name__ vaut "__main__".
    # Si le fichier est importé dans un autre script (avec from wait_for_mongo import wait), __name__ vaut le nom du fichier (wait_for_mongo).
    
    # Création d'un "parser" d'arguments
    # Un parser sert à lire les options qu'on passe au script depuis la ligne de commande
    parser = argparse.ArgumentParser()
    
    # On ajoute des arguments possibles pour le script
    parser.add_argument("--host", default="mongo")   # Nom ou IP du serveur MongoDB
    parser.add_argument("--port", type=int, default=27017)  # Port sur lequel MongoDB écoute
    parser.add_argument("--timeout", type=int, default=60)  # Temps maximum d'attente en secondes
    
    # On récupère les valeurs réelles passées par l'utilisateur
    args = parser.parse_args()
    
    # On appelle notre fonction wait avec ces paramètres
    rc = wait(args.host, args.port, args.timeout)
    
    # On termine le script avec le code de retour renvoyé par wait (0 = succès, 1 = échec)
    sys.exit(rc)
