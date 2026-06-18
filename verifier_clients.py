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
    
    # Voir tous les clients avec leur avocat_id
    cur.execute("SELECT id, avocat_id, nom, prenom FROM client")
    clients = cur.fetchall()
    
    # Voir tous les avocats
    cur.execute("SELECT id_avocat, nom FROM avocat")
    avocats = cur.fetchall()
    
    cx.close()
    
    texte = "=== AVOCATS ===\n"
    for a in avocats:
        texte += f"  id_avocat={a[0]}, nom={a[1]}\n"
    
    texte += "\n=== CLIENTS ===\n"
    if clients:
        for c in clients:
            texte += f"  id={c[0]}, avocat_id={c[1]}, nom={c[2]} {c[3]}\n"
    else:
        texte += "  Aucun client en base !\n"
    
    messagebox.showinfo("Vérification", texte)

except Exception as e:
    messagebox.showerror("Erreur", str(e))

root.destroy()
