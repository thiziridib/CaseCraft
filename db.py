# ============================================================
#  db.py — Connexion centralisée MySQL
# ============================================================
import mysql.connector
from tkinter import messagebox
import json
import os

CFG = dict(host="localhost", user="root", password="", database="gestavocat")

SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".session.json")
SESSION = {"avocat_id": None, "avocat_nom": None}

def sauver_session():
    with open(SESSION_FILE, "w") as f:
        json.dump(SESSION, f)

def charger_session():
    global SESSION
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                SESSION["avocat_id"]  = data.get("avocat_id")
                SESSION["avocat_nom"] = data.get("avocat_nom")
        except Exception:
            pass

def effacer_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    SESSION["avocat_id"]  = None
    SESSION["avocat_nom"] = None

charger_session()

def get_conn():
    return mysql.connector.connect(**CFG)

def query(sql, params=(), fetch=False):
    try:
        cx = get_conn()
        cur = cx.cursor()
        cur.execute(sql, params)
        if fetch:
            rows = cur.fetchall()
            cx.close()
            return rows
        cx.commit()
        cx.close()
        return True
    except Exception as e:
        messagebox.showerror("Erreur base de données", str(e))
        return [] if fetch else False

def init_db():
    ddl = [
        """CREATE TABLE IF NOT EXISTS avocat (
            id_avocat INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255), numero VARCHAR(20), password VARCHAR(255),
            notes TEXT, photo LONGBLOB)""",
        """CREATE TABLE IF NOT EXISTS affaire (
            id INT AUTO_INCREMENT PRIMARY KEY,
            avocat_id INT DEFAULT NULL,
            autorite_judiciaire VARCHAR(255), salle_ou_departement VARCHAR(255),
            type_client VARCHAR(255), nom_client VARCHAR(255), sujet TEXT,
            adversaire VARCHAR(255), remarque TEXT, frais_affaire DECIMAL(10,2),
            type_affaire VARCHAR(255), numero_enquete VARCHAR(50),
            date_depot_dossier DATE, decision_finale VARCHAR(255),
            date VARCHAR(50), cause_romprement TEXT)""",
        """CREATE TABLE IF NOT EXISTS client (
            id INT AUTO_INCREMENT PRIMARY KEY,
            avocat_id INT DEFAULT NULL,
            nom VARCHAR(255), prenom VARCHAR(255), adresse TEXT,
            email VARCHAR(255), telephone VARCHAR(20),
            fichier_nom VARCHAR(255), fichier_contenu LONGBLOB)""",
        """CREATE TABLE IF NOT EXISTS financement (
            id INT AUTO_INCREMENT PRIMARY KEY,
            avocat_id INT DEFAULT NULL,
            Nom_client VARCHAR(255), montant DECIMAL(10,2),
            montant_payee DECIMAL(10,2), montant_restant DECIMAL(10,2),
            date_paiement VARCHAR(50))""",
        """CREATE TABLE IF NOT EXISTS archive (
            id INT AUTO_INCREMENT PRIMARY KEY,
            avocat_id INT DEFAULT NULL,
            autorite_judiciaire VARCHAR(255), departement VARCHAR(255),
            type_client VARCHAR(255), nom_client VARCHAR(255), sujet TEXT,
            adversaire VARCHAR(255), remarque TEXT, frais_affaire DECIMAL(10,2),
            type_affaire VARCHAR(255), numero_enquete VARCHAR(50),
            date_depot DATE, decision_finale VARCHAR(255),
            date_de_rempore VARCHAR(50), cause_romprement TEXT)""",
    ]
    migrations = [
        "ALTER TABLE affaire ADD COLUMN IF NOT EXISTS avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE client ADD COLUMN IF NOT EXISTS avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE financement ADD COLUMN IF NOT EXISTS avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE archive ADD COLUMN IF NOT EXISTS avocat_id INT DEFAULT NULL AFTER id",
    ]
    try:
        cx = get_conn()
        cur = cx.cursor()
        for sql in ddl:
            cur.execute(sql)
        for sql in migrations:
            try: cur.execute(sql)
            except: pass
        cx.commit()
        cx.close()
    except Exception as e:
        messagebox.showerror("Erreur init DB", str(e))