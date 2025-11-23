import hashlib
import json
import os

USERS_FILE = "users.json"

def load_users():
    """
    Charge les utilisateurs depuis le fichier JSON.
    """
    if not os.path.exists(USERS_FILE):
        return {}  # Si le fichier n'existe pas, retourne un dictionnaire vide
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    """
    Sauvegarde la liste des utilisateurs dans le fichier JSON.
    """
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def hash_password(password):
    """
    Retourne un hash du mot de passe.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    """
    Vérifie si le mot de passe correspond au hash.
    """
    return hash_password(password) == hashed

def add_user(username, password):
    """
    Ajoute un nouvel utilisateur avec un mot de passe hashé.
    """
    users = load_users()  # Charge les utilisateurs existants
    if username in users:
        raise ValueError("L'utilisateur existe déjà")
    
    # Hashage du mot de passe
    password_hash = hash_password(password)

    # Ajouter l'utilisateur
    users[username] = {
        "username": username,
        "password_hash": password_hash
    }

    save_users(users)  # Sauvegarde les modifications

