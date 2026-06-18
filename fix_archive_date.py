# fix_archive_date.py — Corrige le type de date_depot dans archive
import mysql.connector
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

try:
    cx = mysql.connector.connect(host="localhost", user="root", password="", database="gestavocat")
    cur = cx.cursor()

    # Changer date_depot de DATE vers VARCHAR pour accepter toutes les valeurs
    cur.execute("ALTER TABLE archive MODIFY COLUMN date_depot_dossier VARCHAR(50)")
    # Changer aussi date_de_rempore
    cur.execute("ALTER TABLE archive MODIFY COLUMN date VARCHAR(50)")
    cx.commit()
    cx.close()

    messagebox.showinfo("✅ Succès", "Table archive corrigée !\nTu peux supprimer ce fichier.")
except Exception as e:
    messagebox.showerror("Erreur", str(e))

root.destroy()
