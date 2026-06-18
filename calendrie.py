import os, sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
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
        "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
        "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
        "FROM affaire WHERE avocat_id=%s ORDER BY date_depot_dossier ASC",
        (avocat_id(),), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def rechercher(event=None):
    terme = e_search.get().strip()
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
        "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
        "FROM affaire WHERE avocat_id=%s AND (nom_client LIKE %s OR adversaire LIKE %s OR type_affaire LIKE %s) "
        "ORDER BY date_depot_dossier ASC",
        (avocat_id(), f"%{terme}%", f"%{terme}%", f"%{terme}%"), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def exporter_pdf():
    path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
    if not path: return
    doc = SimpleDocTemplate(path, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    hdrs = ["ID","Autorité","Salle","Type client","Nom client","Adversaire",
            "Type affaire","Date dépôt","Décision","Date report","Cause"]
    data = [hdrs]
    for rid in tree.get_children():
        data.append(list(tree.item(rid,"values")))
    tbl = Table(data)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0D1B2A")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#1ABC9C")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#1B2A3B")),
        ("TEXTCOLOR",(0,1),(-1,-1),colors.white),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#2C3E50")),
        ("FONTSIZE",(0,0),(-1,-1),8),
    ]))
    doc.build([Paragraph("Calendrier des Affaires", styles["Title"]), Spacer(1,12), tbl])
    messagebox.showinfo("Succès","PDF exporté !")

root = tk.Tk()
root.title("Calendrier")
root.state("zoomed")
T.apply_base(root)
avocat_nom = db.SESSION.get("avocat_nom", "")
T.make_header(root, f"Calendrier  —  {avocat_nom}", back_cmd=lambda: nav("Page1.py"))

main = tk.Frame(root, bg=T.BG); main.pack(fill="both", expand=True)
T.make_sidebar(main, [
    ("📁","Ajouter affaire",  lambda: nav("AjouterAffaire.py")),
    ("🔍","Consulter",        lambda: nav("Consulter.py")),
    ("👤","Clients",          lambda: nav("AjouterClient.py")),
    ("💰","Finances",         lambda: nav("Fainnace.py")),
    ("📅","Calendrier",       lambda: None),
    ("🗄","Archives",         lambda: nav("Archive.py")),
])

content = tk.Frame(main, bg=T.BG); content.pack(fill="both", expand=True, padx=16, pady=14)
toolbar = T.card(content, padx=12, pady=10)
toolbar.pack(fill="x", pady=(0,12))
tk.Label(toolbar, text="🔍", bg=T.BG2, fg=T.CYAN, font=("Segoe UI",13)).pack(side="left",padx=(0,8))
e_search = T.entry(toolbar, w=50)
e_search.pack(side="left", fill="x", expand=True, ipady=6)
e_search.bind("<Return>", rechercher)
T.btn(toolbar, "Rechercher",      cmd=rechercher,    w=14).pack(side="left", padx=6)
T.btn(toolbar, "Actualiser",      cmd=charger,       w=12, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4)
T.btn(toolbar, "📄 Imprimer PDF", cmd=exporter_pdf,  w=16, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4)

T.style_treeview(None)
cols = tuple(range(1,12))
tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=20)
hdrs = ["ID","Autorité","Salle","Type client","Nom client","Adversaire",
        "Type affaire","Date dépôt","Décision","Date report","Cause"]
wds  = [40,120,90,100,120,120,110,100,110,100,120]
for i,(h,w) in enumerate(zip(hdrs,wds),1):
    tree.heading(i,text=h); tree.column(i,width=w,anchor="center")
sb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side="left", fill="both", expand=True)
sb.pack(side="left", fill="y")

charger()
root.mainloop()