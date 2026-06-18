import os, sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import theme as T
import db

def nav(script):
    chemin = os.path.join(os.path.dirname(__file__), script)
    root.destroy()
    subprocess.Popen([sys.executable, chemin])

def charger_clients():
    """Charge les clients de l'avocat connecté dans la combobox."""
    aid = db.SESSION.get("avocat_id")
    rows = db.query(
        "SELECT nom, prenom FROM client WHERE avocat_id=%s ORDER BY nom ASC",
        (aid,), fetch=True)
    if rows:
        liste = [f"{r[0]} {r[1]}" for r in rows]
    else:
        liste = []
    cb_client["values"] = liste

def reset_form():
    cb_client.set("")
    e_adversaire.delete(0, "end")
    cb_autorite.set("")
    cb_dept.set("")
    cb_type_client.set("")
    cb_type_affaire.set("")
    e_frais.delete(0, "end")
    e_enquete.delete(0, "end")
    e_date.delete(0, "end")
    e_decision.delete(0, "end")
    e_report.delete(0, "end")
    e_cause.delete(0, "end")
    t_sujet.delete("1.0", "end")
    t_remarque.delete("1.0", "end")

def ajouter():
    avocat_id = db.SESSION.get("avocat_id")
    if not avocat_id:
        messagebox.showerror("Session", "Aucun avocat connecté.")
        return
    nom_client   = cb_client.get().strip()
    adversaire   = e_adversaire.get().strip()
    if not nom_client or not adversaire:
        messagebox.showwarning("Champs requis", "Nom client et adversaire obligatoires.")
        return
    vals = (
        avocat_id,
        adversaire,
        cb_autorite.get(),
        cb_dept.get(),
        cb_type_client.get(),
        nom_client,
        e_frais.get().strip() or "0",
        cb_type_affaire.get(),
        t_sujet.get("1.0", "end").strip(),
        t_remarque.get("1.0", "end").strip(),
        e_enquete.get().strip(),
        e_date.get().strip() or None,
        e_decision.get().strip(),
        e_report.get().strip(),
        e_cause.get().strip(),
    )
    sql = ("INSERT INTO affaire (avocat_id,adversaire,autorite_judiciaire,salle_ou_departement,"
           "type_client,nom_client,frais_affaire,type_affaire,sujet,remarque,"
           "numero_enquete,date_depot_dossier,decision_finale,date,cause_romprement) "
           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    ok = db.query(sql, vals)
    if ok:
        messagebox.showinfo("Succès", "Affaire ajoutée avec succès.")
        reset_form()

# ── Fenêtre ──────────────────────────────────────────────────
root = tk.Tk()
root.title("Ajouter une affaire")
root.state("zoomed")
T.apply_base(root)

avocat_nom = db.SESSION.get("avocat_nom", "")
T.make_header(root, f"Nouvelle affaire  —  {avocat_nom}", back_cmd=lambda: nav("Page1.py"))

main = tk.Frame(root, bg=T.BG)
main.pack(fill="both", expand=True)

T.make_sidebar(main, [
    ("📁","Ajouter affaire",   lambda: None),
    ("🔍","Consulter",         lambda: nav("Consulter.py")),
    ("👤","Clients",           lambda: nav("AjouterClient.py")),
    ("💰","Finances",          lambda: nav("Fainnace.py")),
    ("📅","Calendrier",        lambda: nav("calendrie.py")),
    ("🗄","Archives",          lambda: nav("Archive.py")),
])

canvas = tk.Canvas(main, bg=T.BG, highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=20, pady=14)
scroll = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
scroll.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scroll.set)

form_outer = tk.Frame(canvas, bg=T.BG)
canvas.create_window((0, 0), window=form_outer, anchor="nw")
form_outer.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def row_fields(parent, label_left, widget_left, label_right=None, widget_right=None):
    r = tk.Frame(parent, bg=T.BG)
    r.pack(fill="x", pady=6)
    lf = tk.Frame(r, bg=T.BG)
    lf.pack(side="left", fill="x", expand=True, padx=(0, 12))
    T.lbl(lf, label_left, size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")
    widget_left.pack(fill="x", ipady=6, pady=2) if isinstance(widget_left, tk.Entry) else widget_left.pack(fill="x", pady=2)
    if label_right and widget_right:
        rf = tk.Frame(r, bg=T.BG)
        rf.pack(side="left", fill="x", expand=True)
        T.lbl(rf, label_right, size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")
        widget_right.pack(fill="x", ipady=6, pady=2) if isinstance(widget_right, tk.Entry) else widget_right.pack(fill="x", pady=2)

T.section_title(form_outer, "Informations générales", bg=T.BG).pack(fill="x", pady=(0, 8))

# ── Nom client = combobox avec clients enregistrés ──
r_client = tk.Frame(form_outer, bg=T.BG)
r_client.pack(fill="x", pady=6)
lf_client = tk.Frame(r_client, bg=T.BG)
lf_client.pack(side="left", fill="x", expand=True, padx=(0, 12))
T.lbl(lf_client, "Nom du client", size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")

cb_frame = tk.Frame(lf_client, bg=T.BG)
cb_frame.pack(fill="x", pady=2)
cb_client = ttk.Combobox(cb_frame, font=("Segoe UI", 11), width=46, state="normal")
cb_client.pack(side="left", fill="x", expand=True, ipady=4)
tk.Button(cb_frame, text="🔄", bg=T.BG2, fg=T.CYAN, relief="flat",
          font=("Segoe UI", 11), cursor="hand2",
          command=charger_clients).pack(side="left", padx=(6,0))

e_adversaire = T.entry(form_outer, w=50)
row_fields(form_outer, "Adversaire", e_adversaire)

cb_autorite = T.combo(form_outer, ["Le tribunal","Le conseil","Cour suprême","Conseil d'état","Tribunal administratif","Cour pénale","Tribunal militaire"])
row_fields(form_outer, "Autorité judiciaire", cb_autorite)
cb_dept = T.combo(form_outer, ["Civiles","Immobilières","Commerciales","Familiales","Pénales"])
row_fields(form_outer, "Département / Salle", cb_dept)

cb_type_client = T.combo(form_outer, ["Demandeur","Accusé","Défendeur","Victime","Fonctionnaire civil"])
row_fields(form_outer, "Type de client", cb_type_client)
cb_type_affaire = T.combo(form_outer, ["Plainte","Convocation directe","Autre"])
row_fields(form_outer, "Type d'affaire", cb_type_affaire)

e_frais = T.entry(form_outer, w=50)
row_fields(form_outer, "Frais d'affaire (DA)", e_frais)
e_enquete = T.entry(form_outer, w=50)
row_fields(form_outer, "Numéro d'enquête", e_enquete)

e_date = T.entry(form_outer, w=50)
row_fields(form_outer, "Date de dépôt (AAAA-MM-JJ)", e_date)
e_decision = T.entry(form_outer, w=50)
row_fields(form_outer, "Décision finale", e_decision)

e_report = T.entry(form_outer, w=50)
row_fields(form_outer, "Date de report", e_report)
e_cause = T.entry(form_outer, w=50)
row_fields(form_outer, "Cause de report", e_cause)

T.section_title(form_outer, "Sujet & Remarques", bg=T.BG).pack(fill="x", pady=(12, 6))
r2 = tk.Frame(form_outer, bg=T.BG); r2.pack(fill="x", pady=4)
lf2 = tk.Frame(r2, bg=T.BG); lf2.pack(side="left", fill="x", expand=True, padx=(0, 12))
T.lbl(lf2, "Sujet", size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")
t_sujet = tk.Text(lf2, height=4, bg=T.BG3, fg=T.TEXT, font=T.FONT_BODY,
                  relief="flat", insertbackground=T.TEXT,
                  highlightbackground=T.BORDER, highlightthickness=1)
t_sujet.pack(fill="x")
rf2 = tk.Frame(r2, bg=T.BG); rf2.pack(side="left", fill="x", expand=True)
T.lbl(rf2, "Remarque", size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")
t_remarque = tk.Text(rf2, height=4, bg=T.BG3, fg=T.TEXT, font=T.FONT_BODY,
                     relief="flat", insertbackground=T.TEXT,
                     highlightbackground=T.BORDER, highlightthickness=1)
t_remarque.pack(fill="x")

btn_row = tk.Frame(form_outer, bg=T.BG); btn_row.pack(fill="x", pady=20)
T.btn(btn_row, "✔  Enregistrer l'affaire", cmd=ajouter, w=30, color=T.SUCCESS, hover="#1E8449").pack(side="left", padx=4, ipady=5)
T.btn(btn_row, "✖  Annuler", cmd=reset_form, w=16, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4, ipady=5)

# Charger les clients au démarrage
charger_clients()

root.mainloop()