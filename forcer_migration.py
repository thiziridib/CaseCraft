# forcer_migration.py — Force l'ajout de avocat_id
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

    commandes = [
        "ALTER TABLE avocat ADD COLUMN avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE affaire ADD COLUMN avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE client ADD COLUMN avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE financement ADD COLUMN avocat_id INT DEFAULT NULL AFTER id",
        "ALTER TABLE archive ADD COLUMN avocat_id INT DEFAULT NULL AFTER id",
    ]

    resultats = []
    for sql in commandes:
        table = sql.split("TABLE ")[1].split(" ")[0]
        try:
            cur.execute(sql)
            cx.commit()
            resultats.append(f"✅ {table} — OK")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                resultats.append(f"⚠️  {table} — déjà présent")
            else:
                resultats.append(f"❌ {table} — {e}")

    cx.close()
    messagebox.showinfo("Résultat", "\n".join(resultats))

except Exception as e:
    messagebox.showerror("Erreur", str(e))

root.destroy()
