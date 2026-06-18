# verifier_db.py — Vérifie la structure de la base
import mysql.connector
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

try:
    cx = mysql.connector.connect(
        host="localhost", user="root", password="", database="gestavocat"
    )
    cur = cx.cursor()

    tables = ["avocat", "affaire", "client", "financement", "archive"]
    rapport = ""

    for table in tables:
        try:
            cur.execute(f"DESCRIBE {table}")
            colonnes = [row[0] for row in cur.fetchall()]
            a_avocat_id = "✅" if "avocat_id" in colonnes else "❌ MANQUANT"
            rapport += f"\n{table}: avocat_id {a_avocat_id}\n"
            rapport += f"  Colonnes: {', '.join(colonnes)}\n"
        except Exception as e:
            rapport += f"\n{table}: ERREUR — {e}\n"

    cx.close()
    messagebox.showinfo("Structure de la base", rapport)

except Exception as e:
    messagebox.showerror("Erreur connexion", str(e))

root.destroy()
