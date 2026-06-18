import os, sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
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

def calculer(event=None):
    try:
        a_payer = float(e_montant.get() or 0)
        paye    = float(e_paye.get() or 0)
        e_restant.config(state="normal")
        e_restant.delete(0, "end")
        e_restant.insert(0, str(round(a_payer - paye, 2)))
        e_restant.config(state="readonly")
    except: pass

def charger():
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id,Nom_client,montant,montant_payee,montant_restant,date_paiement FROM financement WHERE avocat_id=%s",
        (avocat_id(),), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def charger_clients():
    """Charge les clients de l'avocat pour la combobox."""
    rows = db.query(
        "SELECT nom, prenom FROM client WHERE avocat_id=%s ORDER BY nom ASC",
        (avocat_id(),), fetch=True)
    if rows:
        return [f"{r[0]} {r[1]}" for r in rows]
    return []

def on_select(event):
    sel = tree.selection()
    if not sel: return
    v = tree.item(sel[0], "values")
    e_id.config(state="normal"); e_id.delete(0,"end"); e_id.insert(0, v[0])
    cb_nom.set(v[1])
    e_montant.delete(0,"end"); e_montant.insert(0, v[2])
    e_paye.delete(0,"end"); e_paye.insert(0, v[3])
    e_restant.config(state="normal"); e_restant.delete(0,"end"); e_restant.insert(0, v[4])
    e_restant.config(state="readonly")
    e_date.delete(0,"end"); e_date.insert(0, v[5])

def ajouter():
    nom     = cb_nom.get().strip()
    montant = e_montant.get().strip()
    paye    = e_paye.get().strip()
    restant = e_restant.get().strip()
    dat     = e_date.get().strip()
    if not all([nom, montant, paye, dat]):
        messagebox.showwarning("Champs vides", "Remplissez tous les champs requis."); return
    ok = db.query(
        "INSERT INTO financement (avocat_id,Nom_client,montant,montant_payee,montant_restant,date_paiement) "
        "VALUES (%s,%s,%s,%s,%s,%s)",
        (avocat_id(), nom, montant, paye, restant, dat))
    if ok:
        messagebox.showinfo("Succès", "Paiement enregistré !")
        for e in [e_id, e_montant, e_paye, e_date]: e.delete(0, "end")
        cb_nom.set("")
        e_restant.config(state="normal"); e_restant.delete(0,"end"); e_restant.config(state="readonly")
        charger()

def modifier():
    cid = e_id.get().strip()
    if not cid: messagebox.showwarning("Sélection", "Sélectionnez un paiement."); return
    ok = db.query(
        "UPDATE financement SET Nom_client=%s,montant=%s,montant_payee=%s,"
        "montant_restant=%s,date_paiement=%s WHERE id=%s AND avocat_id=%s",
        (cb_nom.get(), e_montant.get(), e_paye.get(),
         e_restant.get(), e_date.get(), cid, avocat_id()))
    if ok: messagebox.showinfo("Succès", "Paiement modifié !"); charger()

def supprimer():
    sel = tree.selection()
    if not sel: messagebox.showwarning("Sélection", "Sélectionnez une ligne."); return
    if messagebox.askyesno("Confirmation", "Supprimer ce paiement ?"):
        cid = tree.item(sel[0], "values")[0]
        db.query("DELETE FROM financement WHERE id=%s AND avocat_id=%s", (cid, avocat_id()))
        charger()

def exporter_pdf():
    path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
    if not path: return
    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()
    data = [["ID","Nom","Montant","Payé","Restant","Date"]]
    for rid in tree.get_children():
        data.append(list(tree.item(rid, "values")))
    tbl = Table(data)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0D1B2A")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#1ABC9C")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#1B2A3B")),
        ("TEXTCOLOR",(0,1),(-1,-1),colors.white),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#2C3E50")),
    ]))
    doc.build([Paragraph("Rapport Financier", styles["Title"]), Spacer(1,12), tbl])
    messagebox.showinfo("Succès", "PDF exporté !")

# ── Fenêtre ──────────────────────────────────────────────────
root = tk.Tk()
root.title("Finances")
root.state("zoomed")
T.apply_base(root)
avocat_nom = db.SESSION.get("avocat_nom", "")
T.make_header(root, f"Gestion Financière  —  {avocat_nom}", back_cmd=lambda: nav("Page1.py"))

main = tk.Frame(root, bg=T.BG); main.pack(fill="both", expand=True)
T.make_sidebar(main, [
    ("📁","Affaires",   lambda: nav("AjouterAffaire.py")),
    ("🔍","Consulter",  lambda: nav("Consulter.py")),
    ("👤","Clients",    lambda: nav("AjouterClient.py")),
    ("💰","Finances",   lambda: None),
    ("📅","Calendrier", lambda: nav("calendrie.py")),
    ("🗄","Archives",   lambda: nav("Archive.py")),
])

content = tk.Frame(main, bg=T.BG); content.pack(fill="both", expand=True, padx=16, pady=14)

form_card = T.card(content, padx=20, pady=16)
form_card.pack(fill="x", pady=(0, 12))
T.section_title(form_card, "Nouveau paiement", bg=T.BG2).pack(fill="x", pady=(0,10))

# Ligne labels
r_labels = tk.Frame(form_card, bg=T.BG2); r_labels.pack(fill="x", pady=(0,2))
for label in ["ID","Nom client","Montant à payer","Montant payé","Date (AAAA-MM-JJ)"]:
    col = tk.Frame(r_labels, bg=T.BG2); col.pack(side="left", fill="x", expand=True, padx=6)
    T.lbl(col, label, size=9, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")

# Ligne champs
r = tk.Frame(form_card, bg=T.BG2); r.pack(fill="x", pady=4)
e_id = T.entry(r, w=8); e_id.pack(side="left", fill="x", expand=True, padx=6, ipady=6)

# Combobox clients
cb_nom = ttk.Combobox(r, font=("Segoe UI", 11), width=18, state="normal")
cb_nom["values"] = charger_clients()
cb_nom.pack(side="left", fill="x", expand=True, padx=6, ipady=4)
tk.Button(r, text="🔄", bg=T.BG2, fg=T.CYAN, relief="flat",
          font=("Segoe UI", 11), cursor="hand2",
          command=lambda: cb_nom.configure(values=charger_clients())).pack(side="left", padx=(0,6))

e_montant = T.entry(r, w=12); e_montant.pack(side="left", fill="x", expand=True, padx=6, ipady=6)
e_montant.bind("<KeyRelease>", calculer)
e_paye = T.entry(r, w=12); e_paye.pack(side="left", fill="x", expand=True, padx=6, ipady=6)
e_paye.bind("<KeyRelease>", calculer)
e_date = T.entry(r, w=14); e_date.pack(side="left", fill="x", expand=True, padx=6, ipady=6)

r2 = tk.Frame(form_card, bg=T.BG2); r2.pack(fill="x", pady=4)
T.lbl(r2, "Montant restant (calculé auto)", size=9, bold=True, color=T.CYAN, bg=T.BG2).pack(anchor="w")
e_restant = T.entry(r2, w=20)
e_restant.pack(anchor="w", ipady=6, pady=2)
e_restant.config(state="readonly")

btn_row = tk.Frame(form_card, bg=T.BG2); btn_row.pack(fill="x", pady=(10,0))
T.btn(btn_row, "➕ Enregistrer", cmd=ajouter,      w=16, color=T.SUCCESS, hover="#1E8449").pack(side="left", padx=4, ipady=4)
T.btn(btn_row, "✏ Modifier",    cmd=modifier,      w=14).pack(side="left", padx=4, ipady=4)
T.btn(btn_row, "🗑 Supprimer",  cmd=supprimer,     w=14, color=T.BG3, hover=T.BORDER, fg=T.ACCENT2).pack(side="left", padx=4, ipady=4)
T.btn(btn_row, "📄 Export PDF", cmd=exporter_pdf,  w=14, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4, ipady=4)

T.style_treeview(None)
cols = (1,2,3,4,5,6)
tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=14)
for i, (h, w) in enumerate(zip(["ID","Nom","Montant","Payé","Restant","Date"],
                                [50, 160, 110, 110, 110, 120]), 1):
    tree.heading(i, text=h); tree.column(i, width=w, anchor="center")
tree.bind("<<TreeviewSelect>>", on_select)
sb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side="left", fill="both", expand=True)
sb.pack(side="left", fill="y")

charger()
root.mainloop()