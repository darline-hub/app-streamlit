import sqlite3 
import hashlib

def connect_db():
    conn = sqlite3.connect('ul.db')
    return conn

conn = connect_db()


#Fonction pour ajouter un utilisateur
def add_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(username, password) VALUES(?,?)',(username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False #Nom d'utilisateur ou email deja pris
    finally:
        conn.close()
    return True

#Fonction pour verifier les identifiants de l'utilisateur
def verify_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?',(username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user is not None

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Util(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE 
        date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tests_debit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        debit_televersement REAL NOT NULL,
        fournisseur TEXT NOT NULL,
        type_connexion TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

# def insert_data(debit, fournisseur, type_connexion, timestamp):
#     """Insère un nouveau test de débit dans la table."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     insert_sql = """
#     INSERT INTO tests_debit (debit_televersement, fournisseur, type_connexion, timestamp)
#     VALUES (?, ?, ?, ?);
#     """
#     cursor.execute(insert_sql, (debit, fournisseur, type_connexion, timestamp))
#     conn.commit()
#     conn.close()
def get_all_data():
    """Récupère toutes les données de la table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tests_debit")
    data = cursor.fetchall()
    conn.close()
    return data

def import_xlsm_to_db(CDR E2E Data report UL.xlsm):
    """Importe les données d'un fichier xlsm dans la base de données."""
    import pandas as pd
    
    try:
        df = pd.read_xlsm(CDR E2E Data report UL.xlsm)
        conn = get_db_connection()
        df.to_sql('tests_debit', conn, if_exists='append', index=False)
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de l'importation du fichier : {e}")
        return False

# Appel de la fonction de création de table lors du premier lancement
create_table()
#Commit et fermeture de la connexion
conn.commit()
conn.close()

        
