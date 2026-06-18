import os, sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import theme as T
import db
import subprocess
from datetime import date

def nav(script):
    chemin = os.path.join(os.path.dirname(__file__), script)
    root.destroy()
    subprocess.Popen([sys.executable, chemin])

def avocat_id():
    return db.SESSION.get("avocat_id")

def charger():
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,"
        "nom_client,adversaire,type_affaire,date_depot_dossier,"
        "decision_finale,date,cause_romprement FROM affaire WHERE avocat_id=%s",
        (avocat_id(),), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def rechercher(event=None):
    terme = e_search.get().strip()
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
        "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
        "FROM affaire WHERE avocat_id=%s AND (nom_client LIKE %s OR adversaire LIKE %s OR type_affaire LIKE %s)",
        (avocat_id(), f"%{terme}%", f"%{terme}%", f"%{terme}%"), fetch=True)
    for r in rows: tree.insert("", "end", values=r)

def supprimer():
    sel = tree.selection()
    if not sel: messagebox.showwarning("Sélection","Sélectionnez une affaire."); return
    if messagebox.askyesno("Confirmation","Supprimer cette affaire ?"):
        cid = tree.item(sel[0],"values")[0]
        db.query("DELETE FROM affaire WHERE id=%s AND avocat_id=%s", (cid, avocat_id()))
        charger()

def archiver_par_id(cid, fen=None):
    aid = avocat_id()
    row = db.query("SELECT * FROM affaire WHERE id=%s AND avocat_id=%s", (cid, aid), fetch=True)
    if row:
        r = row[0]
        # Structure: id, avocat_id, autorite_judiciaire, salle_ou_departement, type_client,
        #            nom_client, sujet, adversaire, remarque, frais_affaire, type_affaire,
        #            numero_enquete, date_depot_dossier, decision_finale, date, cause_romprement
        db.query(
            "INSERT INTO archive (avocat_id,autorite_judiciaire,departement,type_client,nom_client,"
            "sujet,adversaire,remarque,frais_affaire,type_affaire,numero_enquete,"
            "date_depot,decision_finale,date_de_rempore,cause_romprement) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (aid, r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15]))
        db.query("DELETE FROM affaire WHERE id=%s", (cid,))
        if fen: fen.destroy()
        messagebox.showinfo("Archivée","Affaire archivée avec succès !")
        charger()

def archiver():
    sel = tree.selection()
    if not sel: messagebox.showwarning("Sélection","Sélectionnez une affaire."); return
    cid = tree.item(sel[0],"values")[0]
    archiver_par_id(cid)

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
    doc.build([Paragraph("Liste des Affaires", styles["Title"]), Spacer(1,12), tbl])
    messagebox.showinfo("Succès","PDF exporté !")

def afficher_details(event=None):
    sel = tree.selection()
    if not sel: return
    vals = tree.item(sel[0], "values")
    id_affaire = vals[0]

    fen = tk.Toplevel(root)
    fen.title(f"Affaire — {vals[4]}")
    fen.geometry("750x620")
    fen.configure(bg=T.BG)
    fen.grab_set()

    hdr = tk.Frame(fen, bg=T.CYAN, pady=10)
    hdr.pack(fill="x")
    tk.Label(hdr, text=f"⚖  Détails & Modification — ID {id_affaire}",
             bg=T.CYAN, fg=T.BG, font=("Segoe UI", 13, "bold")).pack()

    canvas = tk.Canvas(fen, bg=T.BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(fen, orient="vertical", command=canvas.yview)
    frame_inner = tk.Frame(canvas, bg=T.BG)
    frame_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    labels = [
        ("Autorité judiciaire",  "autorite_judiciaire",  vals[1]),
        ("Salle / Département",  "salle_ou_departement", vals[2]),
        ("Type client",          "type_client",          vals[3]),
        ("Nom client",           "nom_client",           vals[4]),
        ("Adversaire",           "adversaire",           vals[5]),
        ("Type affaire",         "type_affaire",         vals[6]),
        ("Date dépôt dossier",   "date_depot_dossier",   vals[7]),
        ("Décision finale",      "decision_finale",      vals[8]),
        ("Date report",          "date",                 vals[9]),
        ("Cause romprement",     "cause_romprement",     vals[10]),
    ]

    entries = {}
    for i, (label, col, val) in enumerate(labels):
        tk.Label(frame_inner, text=label + " :", bg=T.BG, fg=T.TEXT2,
                 font=("Segoe UI", 10, "bold"), anchor="w").grid(
            row=i, column=0, sticky="w", padx=18, pady=6)
        e = tk.Entry(frame_inner, font=("Segoe UI", 10), bg=T.BG2,
                     fg=T.TEXT, insertbackground=T.CYAN,
                     relief="flat", bd=0, highlightthickness=1,
                     highlightbackground=T.BORDER, highlightcolor=T.CYAN, width=42)
        e.insert(0, val if val else "")
        e.grid(row=i, column=1, padx=14, pady=6, ipady=5, sticky="w")
        entries[col] = e

    btn_frame = tk.Frame(fen, bg=T.BG2, pady=12)
    btn_frame.pack(fill="x", side="bottom")

    def valider_modification():
        nouvelles = {col: e.get().strip() for col, e in entries.items()}
        db.query(
            "UPDATE affaire SET autorite_judiciaire=%s, salle_ou_departement=%s, "
            "type_client=%s, nom_client=%s, adversaire=%s, type_affaire=%s, "
            "date_depot_dossier=%s, decision_finale=%s, date=%s, cause_romprement=%s "
            "WHERE id=%s AND avocat_id=%s",
            (nouvelles["autorite_judiciaire"], nouvelles["salle_ou_departement"],
             nouvelles["type_client"], nouvelles["nom_client"], nouvelles["adversaire"],
             nouvelles["type_affaire"], nouvelles["date_depot_dossier"],
             nouvelles["decision_finale"], nouvelles["date"], nouvelles["cause_romprement"],
             id_affaire, avocat_id()))
        messagebox.showinfo("Succès", "Affaire modifiée avec succès !")
        fen.destroy()
        charger()

    def remporter_affaire():
        aujourd_hui = date.today().strftime("%Y-%m-%d")
        if messagebox.askyesno("Remporter", f"Confirmer REMPORTÉE le {aujourd_hui} ?"):
            db.query("UPDATE affaire SET decision_finale=%s, date=%s WHERE id=%s AND avocat_id=%s",
                     ("Gagnée", aujourd_hui, id_affaire, avocat_id()))
            entries["decision_finale"].delete(0, tk.END)
            entries["decision_finale"].insert(0, "Gagnée")
            entries["date"].delete(0, tk.END)
            entries["date"].insert(0, aujourd_hui)
            messagebox.showinfo("🏆", "L'affaire a été marquée comme GAGNÉE !")
            charger()

    def saisir_decision():
        win = tk.Toplevel(fen)
        win.title("Saisir la décision")
        win.geometry("420x220")
        win.configure(bg=T.BG)
        win.grab_set()
        tk.Label(win, text="Décision finale :", bg=T.BG, fg=T.TEXT2,
                 font=("Segoe UI", 10, "bold")).pack(pady=(18,4))
        e_dec = tk.Entry(win, font=("Segoe UI", 11), bg=T.BG2, fg=T.TEXT,
                         insertbackground=T.CYAN, relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=T.BORDER,
                         highlightcolor=T.CYAN, width=36)
        e_dec.insert(0, entries["decision_finale"].get())
        e_dec.pack(ipady=6, pady=4)
        tk.Label(win, text="Date de la décision :", bg=T.BG, fg=T.TEXT2,
                 font=("Segoe UI", 10, "bold")).pack(pady=(10,4))
        e_date = tk.Entry(win, font=("Segoe UI", 11), bg=T.BG2, fg=T.TEXT,
                          insertbackground=T.CYAN, relief="flat", bd=0,
                          highlightthickness=1, highlightbackground=T.BORDER,
                          highlightcolor=T.CYAN, width=36)
        e_date.insert(0, entries["date"].get() or date.today().strftime("%Y-%m-%d"))
        e_date.pack(ipady=6, pady=4)
        def confirmer_decision():
            dec = e_dec.get().strip()
            dat = e_date.get().strip()
            if not dec:
                messagebox.showwarning("Champ vide", "Veuillez saisir la décision.")
                return
            db.query("UPDATE affaire SET decision_finale=%s, date=%s WHERE id=%s AND avocat_id=%s",
                     (dec, dat, id_affaire, avocat_id()))
            entries["decision_finale"].delete(0, tk.END)
            entries["decision_finale"].insert(0, dec)
            entries["date"].delete(0, tk.END)
            entries["date"].insert(0, dat)
            messagebox.showinfo("Décision enregistrée", "La décision a été mise à jour.")
            win.destroy()
            charger()
        tk.Button(win, text="✔ Confirmer", command=confirmer_decision,
                  bg=T.CYAN, fg=T.BG, font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=18, pady=6, cursor="hand2").pack(pady=14)

    def archiver_depuis_details():
        if messagebox.askyesno("Archiver", "Archiver cette affaire ?"):
            archiver_par_id(id_affaire, fen)

    tk.Button(btn_frame, text="✏️  Modifier", command=valider_modification,
              bg=T.CYAN, fg=T.BG, font=("Segoe UI", 10, "bold"),
              relief="flat", padx=16, pady=7, cursor="hand2").pack(side="left", padx=12)
    tk.Button(btn_frame, text="🏆  Remporter affaire", command=remporter_affaire,
              bg="#27AE60", fg="white", font=("Segoe UI", 10, "bold"),
              relief="flat", padx=16, pady=7, cursor="hand2").pack(side="left", padx=8)
    tk.Button(btn_frame, text="⚖️  Décision", command=saisir_decision,
              bg="#2980B9", fg="white", font=("Segoe UI", 10, "bold"),
              relief="flat", padx=16, pady=7, cursor="hand2").pack(side="left", padx=8)
    tk.Button(btn_frame, text="🗄  Archiver", command=archiver_depuis_details,
              bg="#8E44AD", fg="white", font=("Segoe UI", 10, "bold"),
              relief="flat", padx=16, pady=7, cursor="hand2").pack(side="left", padx=8)
    tk.Button(btn_frame, text="✖  Fermer", command=fen.destroy,
              bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 10),
              relief="flat", padx=16, pady=7, cursor="hand2").pack(side="right", padx=12)

# ── Fenêtre principale ──────────────────────────────────────
root = tk.Tk()
root.title("Consulter affaires")
root.state("zoomed")
T.apply_base(root)
avocat_nom = db.SESSION.get("avocat_nom", "")
T.make_header(root, f"Consulter les affaires  —  {avocat_nom}", back_cmd=lambda: nav("Page1.py"))

main = tk.Frame(root, bg=T.BG); main.pack(fill="both", expand=True)
T.make_sidebar(main, [
    ("📁","Ajouter affaire",  lambda: nav("AjouterAffaire.py")),
    ("🔍","Consulter",        lambda: None),
    ("👤","Clients",          lambda: nav("AjouterClient.py")),
    ("💰","Finances",         lambda: nav("Fainnace.py")),
    ("📅","Calendrier",       lambda: nav("calendrie.py")),
    ("🗄","Archives",         lambda: nav("Archive.py")),
])

content = tk.Frame(main, bg=T.BG); content.pack(fill="both", expand=True, padx=16, pady=14)

toolbar = T.card(content, padx=12, pady=10)
toolbar.pack(fill="x", pady=(0,12))
tk.Label(toolbar, text="🔍", bg=T.BG2, fg=T.CYAN, font=("Segoe UI",13)).pack(side="left", padx=(0,8))
e_search = T.entry(toolbar, w=50)
e_search.pack(side="left", fill="x", expand=True, ipady=6)
e_search.bind("<Return>", rechercher)
T.btn(toolbar, "Rechercher",   cmd=rechercher,  w=14).pack(side="left", padx=6)
T.btn(toolbar, "Actualiser",   cmd=charger,     w=12, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4)
T.btn(toolbar, "🗑 Supprimer", cmd=supprimer,   w=14, color=T.BG3, hover=T.BORDER, fg=T.ACCENT2).pack(side="left", padx=4)
T.btn(toolbar, "🗄 Archiver",  cmd=archiver,    w=14, color=T.BG3, hover=T.BORDER, fg=T.CYAN).pack(side="left", padx=4)
T.btn(toolbar, "📄 PDF",       cmd=exporter_pdf,w=10, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4)

T.style_treeview(None)
cols = tuple(range(1, 12))
tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=20)
hdrs = ["ID","Autorité","Salle","Type client","Nom client","Adversaire",
        "Type affaire","Date dépôt","Décision","Date report","Cause"]
wds  = [40, 120, 90, 100, 120, 120, 110, 100, 110, 100, 120]
for i,(h,w) in enumerate(zip(hdrs,wds),1):
    tree.heading(i,text=h); tree.column(i,width=w,anchor="center")
sb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side="left", fill="both", expand=True)
sb.pack(side="left", fill="y")

tree.bind("<Double-1>", afficher_details)
charger()
root.mainloop()