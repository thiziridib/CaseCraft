import os, sys
import tkinter as tk
from tkinter import ttk, messagebox
import theme as T
import db
import subprocess

def nav(script):
    chemin = os.path.join(os.path.dirname(__file__), script)
    root.destroy()
    subprocess.Popen([sys.executable, chemin])

def charger():
    aid = db.SESSION.get("avocat_id")
    for i in tree.get_children(): tree.delete(i)
    rows = db.query("SELECT * FROM archive WHERE avocat_id=%s", (aid,), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def supprimer():
    aid = db.SESSION.get("avocat_id")
    sel = tree.selection()
    if not sel: messagebox.showwarning("Sélection","Sélectionnez une archive."); return
    if messagebox.askyesno("Confirmation","Supprimer cette archive ?"):
        cid = tree.item(sel[0],"values")[0]
        db.query("DELETE FROM archive WHERE id=%s AND avocat_id=%s", (cid, aid))
        charger()

def filtrer():
    aid = db.SESSION.get("avocat_id")
    import tkinter.simpledialog as sd
    val = sd.askstring("Filtrer","Entrez un nom de client à rechercher:")
    if val:
        for i in tree.get_children(): tree.delete(i)
        rows = db.query("SELECT * FROM archive WHERE avocat_id=%s AND nom_client LIKE %s",
                        (aid, f"%{val}%"), fetch=True)
        for r in rows: tree.insert("","end",values=r)

root = tk.Tk()
root.title("Archives")
root.state("zoomed")
T.apply_base(root)
avocat_nom = db.SESSION.get("avocat_nom", "")
T.make_header(root, f"Archives  —  {avocat_nom}", back_cmd=lambda: nav("Page1.py"))

main = tk.Frame(root, bg=T.BG); main.pack(fill="both", expand=True)
T.make_sidebar(main, [
    ("📁","Ajouter affaire",  lambda: nav("AjouterAffaire.py")),
    ("🔍","Consulter",        lambda: nav("Consulter.py")),
    ("👤","Clients",          lambda: nav("AjouterClient.py")),
    ("💰","Finances",         lambda: nav("Fainnace.py")),
    ("📅","Calendrier",       lambda: nav("calendrie.py")),
    ("🗄","Archives",         lambda: None),
])

content = tk.Frame(main, bg=T.BG); content.pack(fill="both", expand=True, padx=16, pady=14)

toolbar = T.card(content, padx=12, pady=10)
toolbar.pack(fill="x", pady=(0,12))
T.btn(toolbar, "🗑 Supprimer", cmd=supprimer, w=14, color=T.BG3, hover=T.BORDER, fg=T.ACCENT2).pack(side="left",padx=4)
T.btn(toolbar, "🔍 Filtrer",  cmd=filtrer,   w=14, color=T.BG3, hover=T.BORDER, fg=T.CYAN).pack(side="left",padx=4)
T.btn(toolbar, "Actualiser",   cmd=charger,   w=12, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left",padx=4)

T.style_treeview(None)
cols = tuple(range(1,17))
tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=20)
hdrs = ["ID","Avocat ID","Autorité","Dép.","Type client","Nom client","Sujet","Adversaire",
        "Remarque","Frais","Type affaire","N° enquête","Date dépôt",
        "Décision","Date report","Cause"]
wds  = [40,0,100,80,90,110,100,110,100,70,100,80,90,110,90,110]
for i,(h,w) in enumerate(zip(hdrs,wds),1):
    tree.heading(i,text=h); tree.column(i,width=w,anchor="center")
# Cacher la colonne avocat_id
tree.column(2, width=0, minwidth=0, stretch=False)
sb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side="left", fill="both", expand=True)
sb.pack(side="left", fill="y")

charger()
root.mainloop()