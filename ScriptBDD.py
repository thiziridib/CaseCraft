import mysql.connector
from tkinter import messagebox

def get_connexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestavocat"
    )

def init_db():
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    curseur = connexion.cursor()
    curseur.execute("CREATE DATABASE IF NOT EXISTS gestavocat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    curseur.execute("USE gestavocat")

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS avocat (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(255) NOT NULL,
        numero VARCHAR(20),
        password VARCHAR(255) NOT NULL
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS affaire (
        id INT AUTO_INCREMENT PRIMARY KEY,
        autorite_judiciaire VARCHAR(255),
        salle_ou_departement VARCHAR(255),
        type_client VARCHAR(255),
        nom_client VARCHAR(255),
        sujet TEXT,
        adversaire VARCHAR(255),
        remarque TEXT,
        frais_affaire DECIMAL(10,2),
        type_affaire VARCHAR(255),
        numero_enquete VARCHAR(50),
        date_depot_dossier DATE,
        decision_finale TEXT,
        date DATE,
        cause_romprement TEXT
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS client (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(255),
        prenom VARCHAR(255),
        adresse TEXT,
        email VARCHAR(255),
        telephone VARCHAR(20),
        fichier_nom VARCHAR(255),
        fichier_contenu LONGBLOB
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS financement (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Nom_client VARCHAR(255),
        montant DECIMAL(10,2),
        montant_payee DECIMAL(10,2),
        montant_restant DECIMAL(10,2),
        date_paiement DATE
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS archive (
        id INT AUTO_INCREMENT PRIMARY KEY,
        autorite_judiciaire VARCHAR(255),
        salle_ou_departement VARCHAR(255),
        type_client VARCHAR(255),
        nom_client VARCHAR(255),
        sujet TEXT,
        adversaire VARCHAR(255),
        remarque TEXT,
        frais_affaire DECIMAL(10,2),
        type_affaire VARCHAR(255),
        numero_enquete VARCHAR(50),
        date_depot_dossier DATE,
        decision_finale TEXT,
        date DATE,
        cause_romprement TEXT
    )
    """)

    connexion.commit()
    curseur.close()
    connexion.close()

# Initialiser la base au démarrage
try:
    init_db()
except Exception as e:
    print(f"Erreur init DB: {e}")
