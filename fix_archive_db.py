# fix_archive_db.py — Corrige la table archive
# Lance ce fichier UNE SEULE FOIS
import mysql.connector
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

try:
    cx = mysql.connector.connect(host="localhost", user="root", password="", database="gestavocat")
    cur = cx.cursor()

    # Vérifier si la colonne s'appelle 'departement' ou 'salle_ou_departement'
    cur.execute("SHOW COLUMNS FROM archive LIKE 'salle_ou_departement'")
    if cur.fetchone():
        # Renommer la colonne
        cur.execute("ALTER TABLE archive CHANGE salle_ou_departement salle_ou_departement VARCHAR(255)")
        cx.commit()
        messagebox.showinfo("✅ Succès", "Colonne renommée avec succès !\nTu peux supprimer ce fichier.")
    else:
        cur.execute("SHOW COLUMNS FROM archive LIKE 'salle_ou_departement'")
        if cur.fetchone():
            messagebox.showinfo("✅ Déjà correct", "La colonne est déjà correcte !")
        else:
            cur.execute("ALTER TABLE archive ADD COLUMN salle_ou_departement VARCHAR(255)")
            cx.commit()
            messagebox.showinfo("✅ Ajoutée", "Colonne ajoutée avec succès !")

    cx.close()
except Exception as e:
    messagebox.showerror("Erreur", str(e))

root.destroy()
