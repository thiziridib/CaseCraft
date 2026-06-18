import os, sys
import tkinter as tk
from tkinter import messagebox
import theme as T
import db

def ouvrir_page1():
    root.destroy()
    import subprocess
    chemin = os.path.join(os.path.dirname(__file__), "Page1.py")
    subprocess.Popen([sys.executable, chemin])

def ouvrir_inscription():
    root.destroy()
    import subprocess
    chemin = os.path.join(os.path.dirname(__file__), "inscription.py")
    subprocess.Popen([sys.executable, chemin])

def valider():
    nom = e_nom.get().strip()
    mdp = e_mdp.get().strip()
    if not nom or not mdp:
        messagebox.showwarning("Champs vides", "Remplissez tous les champs.")
        return
    rows = db.query("SELECT id_avocat, nom FROM avocat WHERE nom=%s AND password=%s",
                    (nom, mdp), fetch=True)
    if rows:
        db.SESSION["avocat_id"]  = rows[0][0]
        db.SESSION["avocat_nom"] = rows[0][1]
        db.sauver_session()  # ← Sauvegarde dans le fichier
        messagebox.showinfo("Succès", f"Bienvenue, {rows[0][1]} !")
        ouvrir_page1()
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects.")

db.init_db()
root = tk.Tk()
root.title("CaseCraft — Connexion")
root.geometry("900x600")
root.resizable(False, False)
T.apply_base(root)

left = tk.Frame(root, bg=T.BG3, width=360)
left.pack(fill="y", side="left")
left.pack_propagate(False)
tk.Label(left, text="⚖", bg=T.BG3, fg=T.CYAN, font=("Segoe UI", 60)).pack(pady=(80, 10))
tk.Label(left, text="CaseCraft", bg=T.BG3, fg=T.WHITE, font=("Segoe UI", 28, "bold")).pack()
tk.Label(left, text="Gestion Cabinet d'Avocat", bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 11)).pack(pady=4)
tk.Frame(left, bg=T.BORDER, height=1, width=200).pack(pady=20)
tk.Label(left, text='"La justice est le fondement\nde toute société équitable."',
         bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 10, "italic"), justify="center").pack(padx=20)

right = tk.Frame(root, bg=T.BG)
right.pack(fill="both", expand=True)
form = T.card(right, padx=40, pady=40)
form.place(relx=0.5, rely=0.5, anchor="center", width=380, height=380)

T.lbl(form, "Bienvenue", size=18, bold=True, color=T.WHITE, bg=T.BG2).pack(pady=(0, 4))
T.lbl(form, "Connectez-vous à votre espace", size=10, color=T.TEXT2, bg=T.BG2).pack(pady=(0, 24))
T.lbl(form, "Nom d'utilisateur", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
e_nom = T.entry(form, w=32)
e_nom.pack(fill="x", pady=(4, 14), ipady=7)
T.lbl(form, "Mot de passe", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
e_mdp = T.entry(form, w=32, show="•")
e_mdp.pack(fill="x", pady=(4, 20), ipady=7)
root.bind("<Return>", lambda e: valider())
T.btn(form, "Se connecter", cmd=valider, w=32).pack(fill="x", ipady=4)

link_frame = tk.Frame(form, bg=T.BG2)
link_frame.pack(pady=(14, 0))
T.lbl(link_frame, "Pas de compte ?", size=9, color=T.TEXT2, bg=T.BG2).pack(side="left")
lnk = T.lbl(link_frame, "  S'inscrire", size=9, bold=True, color=T.CYAN, bg=T.BG2)
lnk.pack(side="left")
lnk.bind("<Button-1>", lambda e: ouvrir_inscription())
lnk.config(cursor="hand2")

root.mainloop()