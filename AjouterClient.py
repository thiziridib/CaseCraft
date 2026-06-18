import os, sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import theme as T
import db
import subprocess

def nav(script):
    chemin = os.path.join(os.path.dirname(__file__), script)
    root.destroy()
    subprocess.Popen([sys.executable, chemin])

def avocat_id():
    return db.SESSION.get("avocat_id")

def charger():
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id,nom,prenom,adresse,email,telephone,fichier_nom FROM client WHERE avocat_id=%s",
        (avocat_id(),), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def on_select(event):
    sel = tree.selection()
    if not sel: return
    v = tree.item(sel[0], "values")
    for e, val in zip([e_id, e_nom, e_prenom, e_adresse, e_email, e_tel], v):
        e.config(state="normal"); e.delete(0, "end"); e.insert(0, val)

def ajouter():
    nom    = e_nom.get().strip()
    prenom = e_prenom.get().strip()
    adresse= e_adresse.get().strip()
    email  = e_email.get().strip()
    tel    = e_tel.get().strip()
    if not all([nom, prenom, adresse, email, tel]):
        messagebox.showwarning("Champs vides", "Remplissez tous les champs."); return
    ok = db.query(
        "INSERT INTO client (avocat_id,nom,prenom,adresse,email,telephone) VALUES (%s,%s,%s,%s,%s,%s)",
        (avocat_id(), nom, prenom, adresse, email, tel))
    if ok:
        messagebox.showinfo("Succès", "Client ajouté !")
        for e in [e_nom, e_prenom, e_adresse, e_email, e_tel]: e.delete(0, "end")
        charger()

def modifier():
    cid = e_id.get().strip()
    if not cid: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
    nom    = e_nom.get().strip()
    prenom = e_prenom.get().strip()
    adresse= e_adresse.get().strip()
    email  = e_email.get().strip()
    tel    = e_tel.get().strip()
    ok = db.query(
        "UPDATE client SET nom=%s,prenom=%s,adresse=%s,email=%s,telephone=%s WHERE id=%s AND avocat_id=%s",
        (nom, prenom, adresse, email, tel, cid, avocat_id()))
    if ok: messagebox.showinfo("Succès", "Client modifié !"); charger()

def supprimer():
    sel = tree.selection()
    if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
    if messagebox.askyesno("Confirmation", "Supprimer ce client ?"):
        cid = tree.item(sel[0], "values")[0]
        db.query("DELETE FROM client WHERE id=%s AND avocat_id=%s", (cid, avocat_id()))
        charger()

def joindre():
    sel = tree.selection()
    if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
    cid = tree.item(sel[0], "values")[0]
    path = filedialog.askopenfilename()
    if path:
        nom_f = os.path.basename(path)
        with open(path, "rb") as fh: contenu = fh.read()
        db.query("UPDATE client SET fichier_nom=%s, fichier_contenu=%s WHERE id=%s AND avocat_id=%s",
                 (nom_f, contenu, cid, avocat_id()))
        messagebox.showinfo("Succès", "Fichier joint !")
        charger()

# ── Fenêtre ──────────────────────────────────────────────────
root = tk.Tk()
root.title("Gestion Clients")
root.state("zoomed")
T.apply_base(root)
avocat_nom = db.SESSION.get("avocat_nom", "")
T.make_header(root, f"Clients  —  {avocat_nom}", back_cmd=lambda: nav("Page1.py"))

main = tk.Frame(root, bg=T.BG); main.pack(fill="both", expand=True)
T.make_sidebar(main, [
    ("📁","Affaires",   lambda: nav("AjouterAffaire.py")),
    ("🔍","Consulter",  lambda: nav("Consulter.py")),
    ("👤","Clients",    lambda: None),
    ("💰","Finances",   lambda: nav("Fainnace.py")),
    ("📅","Calendrier", lambda: nav("calendrie.py")),
    ("🗄","Archives",   lambda: nav("Archive.py")),
])

content = tk.Frame(main, bg=T.BG); content.pack(fill="both", expand=True, padx=16, pady=14)

form_card = T.card(content, padx=20, pady=16)
form_card.pack(fill="x", pady=(0, 12))
T.section_title(form_card, "Informations client", bg=T.BG2).pack(fill="x", pady=(0, 10))

def field_row(parent, items):
    r = tk.Frame(parent, bg=T.BG2); r.pack(fill="x", pady=4)
    entries = []
    for label, show in items:
        f = tk.Frame(r, bg=T.BG2); f.pack(side="left", fill="x", expand=True, padx=4)
        T.lbl(f, label, size=9, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        e = T.entry(f, w=24, show=show)
        e.pack(fill="x", ipady=6, pady=2)
        entries.append(e)
    return entries

e_id_frame = tk.Frame(form_card, bg=T.BG2); e_id_frame.pack(fill="x", pady=(0,6))
T.lbl(e_id_frame, "ID (rempli auto à la sélection)", size=9, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
e_id = T.entry(e_id_frame, w=20)
e_id.pack(anchor="w", ipady=6, pady=2)
e_id.config(state="disabled")

(e_nom, e_prenom), = [field_row(form_card, [("Nom",""),("Prénom","")])]
(e_adresse, e_email), = [field_row(form_card, [("Adresse",""),("Email","")])]
(e_tel,), = [field_row(form_card, [("Téléphone","")])]

btn_row = tk.Frame(form_card, bg=T.BG2); btn_row.pack(fill="x", pady=(12, 0))
T.btn(btn_row, "➕ Ajouter",        cmd=ajouter,   w=16, color=T.SUCCESS, hover="#1E8449").pack(side="left", padx=4, ipady=4)
T.btn(btn_row, "✏ Modifier",       cmd=modifier,  w=16).pack(side="left", padx=4, ipady=4)
T.btn(btn_row, "🗑 Supprimer",     cmd=supprimer, w=16, color=T.BG3, hover=T.BORDER, fg=T.ACCENT2).pack(side="left", padx=4, ipady=4)
T.btn(btn_row, "📎 Joindre fichier",cmd=joindre,   w=18, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4, ipady=4)

T.style_treeview(None)
cols = (1,2,3,4,5,6,7)
tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=14)
hdrs = ["ID","Nom","Prénom","Adresse","Email","Téléphone","Document"]
wds  = [40, 120, 120, 160, 160, 110, 130]
for i, (h, w) in enumerate(zip(hdrs, wds), 1):
    tree.heading(i, text=h); tree.column(i, width=w, anchor="center")
tree.bind("<<TreeviewSelect>>", on_select)
sb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side="left", fill="both", expand=True)
sb.pack(side="left", fill="y")

e_id.config(state="normal")
charger()
root.mainloop()