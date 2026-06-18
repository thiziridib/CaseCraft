import os, sys
import tkinter as tk
from tkinter import messagebox
import theme as T
import db

def retour():
    root.destroy()
    import subprocess
    chemin = os.path.join(os.path.dirname(__file__), "HomePage.py")
    subprocess.Popen([sys.executable, chemin])

def valider():
    nom = e_nom.get().strip()
    num = e_num.get().strip()
    mdp = e_mdp.get().strip()
    if not nom or not num or not mdp:
        messagebox.showwarning("Champs vides", "Remplissez tous les champs.")
        return
    if not num.isdigit():
        messagebox.showerror("Erreur", "Le numéro doit contenir uniquement des chiffres.")
        return
    # Vérifie si le nom existe déjà
    existe = db.query("SELECT id_avocat FROM avocat WHERE nom=%s", (nom,), fetch=True)
    if existe:
        messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
        return
    ok = db.query("INSERT INTO avocat (nom, numero, password) VALUES (%s,%s,%s)",
                  (nom, num, mdp))
    if ok:
        messagebox.showinfo("Succès", "Inscription réussie ! Connectez-vous maintenant.")
        retour()

db.init_db()
root = tk.Tk()
root.title("CaseCraft — Inscription")
root.geometry("900x600")
root.resizable(False, False)
T.apply_base(root)

left = tk.Frame(root, bg=T.BG3, width=360)
left.pack(fill="y", side="left")
left.pack_propagate(False)
tk.Label(left, text="⚖", bg=T.BG3, fg=T.CYAN, font=("Segoe UI", 60)).pack(pady=(80, 10))
tk.Label(left, text="CaseCraft", bg=T.BG3, fg=T.WHITE, font=("Segoe UI", 28, "bold")).pack()
tk.Label(left, text="Créer un compte avocat", bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 11)).pack(pady=4)

right = tk.Frame(root, bg=T.BG)
right.pack(fill="both", expand=True)
form = T.card(right, padx=40, pady=40)
form.place(relx=0.5, rely=0.5, anchor="center", width=380, height=400)

T.lbl(form, "Inscription", size=18, bold=True, color=T.WHITE, bg=T.BG2).pack(pady=(0, 20))
T.lbl(form, "Nom", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
e_nom = T.entry(form, w=32)
e_nom.pack(fill="x", pady=(4, 12), ipady=7)
T.lbl(form, "Numéro", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
e_num = T.entry(form, w=32)
e_num.pack(fill="x", pady=(4, 12), ipady=7)
T.lbl(form, "Mot de passe", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
e_mdp = T.entry(form, w=32, show="•")
e_mdp.pack(fill="x", pady=(4, 20), ipady=7)
T.btn(form, "Créer le compte", cmd=valider, w=32).pack(fill="x", ipady=4)

link_frame = tk.Frame(form, bg=T.BG2)
link_frame.pack(pady=(12, 0))
T.lbl(link_frame, "Déjà un compte ?", size=9, color=T.TEXT2, bg=T.BG2).pack(side="left")
lnk = T.lbl(link_frame, "  Se connecter", size=9, bold=True, color=T.CYAN, bg=T.BG2)
lnk.pack(side="left")
lnk.bind("<Button-1>", lambda e: retour())
lnk.config(cursor="hand2")

root.mainloop()