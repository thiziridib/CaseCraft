# ============================================================
#  migration.py — Ajoute avocat_id aux tables existantes
#  Lance ce fichier UNE SEULE FOIS puis supprime-le
# ============================================================
import mysql.connector
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()  # Cache la fenêtre tkinter

try:
    cx = mysql.connector.connect(
        host="localhost", user="root", password="", database="gestavocat"
    )
    cur = cx.cursor()

    migrations = [
        ("affaire",     "ALTER TABLE affaire ADD COLUMN avocat_id INT DEFAULT NULL AFTER id"),
        ("client",      "ALTER TABLE client ADD COLUMN avocat_id INT DEFAULT NULL AFTER id"),
        ("financement", "ALTER TABLE financement ADD COLUMN avocat_id INT DEFAULT NULL AFTER id"),
        ("archive",     "ALTER TABLE archive ADD COLUMN avocat_id INT DEFAULT NULL AFTER id"),
    ]

    resultats = []
    for table, sql in migrations:
        try:
            cur.execute(sql)
            resultats.append(f"✅ {table} — colonne avocat_id ajoutée")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                resultats.append(f"⚠️  {table} — avocat_id existe déjà (ok)")
            else:
                resultats.append(f"❌ {table} — ERREUR : {e}")

    cx.commit()
    cx.close()

    messagebox.showinfo(
        "Migration terminée",
        "\n".join(resultats) + "\n\nTu peux supprimer ce fichier maintenant."
    )

except Exception as e:
    messagebox.showerror("Erreur de connexion", str(e))

root.destroy()
