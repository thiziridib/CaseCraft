import os, sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import theme as T
import db
import subprocess
from PIL import Image, ImageTk, ImageDraw
import io

def nav(script):
    chemin = os.path.join(os.path.dirname(__file__), script)
    root.destroy()
    subprocess.Popen([sys.executable, chemin])

def deconnexion():
    if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
        db.effacer_session()
        nav("HomePage.py")

def verifier_alertes():
    aid = db.SESSION.get("avocat_id")
    rows = db.query(
        "SELECT nom_client, date_depot_dossier FROM affaire "
        "WHERE avocat_id=%s AND DATEDIFF(date_depot_dossier, CURDATE()) BETWEEN 0 AND 5",
        (aid,), fetch=True)
    if rows:
        msg = "⚠ Audiences dans les 5 prochains jours :\n\n"
        for nom, d in rows: msg += f"• {nom}  →  {d}\n"
        messagebox.showwarning("Alerte audiences", msg)

def charger_affaires():
    aid = db.SESSION.get("avocat_id")
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id, autorite_judiciaire, salle_ou_departement, type_client, "
        "nom_client, adversaire, type_affaire, date_depot_dossier, decision_finale, "
        "date, cause_romprement FROM affaire WHERE avocat_id=%s", (aid,), fetch=True)
    for row in rows: tree.insert("", "end", values=row)

def rechercher(event=None):
    aid = db.SESSION.get("avocat_id")
    terme = e_search.get().strip()
    for i in tree.get_children(): tree.delete(i)
    rows = db.query(
        "SELECT id, autorite_judiciaire, salle_ou_departement, type_client, "
        "nom_client, adversaire, type_affaire, date_depot_dossier, decision_finale, "
        "date, cause_romprement FROM affaire "
        "WHERE avocat_id=%s AND (nom_client LIKE %s OR adversaire LIKE %s OR type_affaire LIKE %s)",
        (aid, f"%{terme}%", f"%{terme}%", f"%{terme}%"), fetch=True)
    for row in rows: tree.insert("", "end", values=row)

def count(table):
    aid = db.SESSION.get("avocat_id")
    rows = db.query(f"SELECT COUNT(*) FROM {table} WHERE avocat_id=%s", (aid,), fetch=True)
    return rows[0][0] if rows else 0

def count_gagnees():
    aid = db.SESSION.get("avocat_id")
    rows = db.query(
        "SELECT COUNT(*) FROM affaire WHERE avocat_id=%s AND decision_finale='Gagnée'",
        (aid,), fetch=True)
    return rows[0][0] if rows else 0

def montant_total():
    aid = db.SESSION.get("avocat_id")
    rows = db.query(
        "SELECT SUM(montant), SUM(montant_payee), SUM(montant_restant) FROM financement WHERE avocat_id=%s",
        (aid,), fetch=True)
    if rows and rows[0][0]:
        return rows[0]
    return (0, 0, 0)

def migration_colonnes():
    try:
        cx = db.get_conn()
        cur = cx.cursor()
        cur.execute("SHOW COLUMNS FROM avocat LIKE 'notes'")
        if not cur.fetchone():
            cur.execute("ALTER TABLE avocat ADD COLUMN notes TEXT")
        cur.execute("SHOW COLUMNS FROM avocat LIKE 'photo'")
        if not cur.fetchone():
            cur.execute("ALTER TABLE avocat ADD COLUMN photo LONGBLOB")
        cx.commit()
        cx.close()
    except Exception as e:
        print(f"Migration: {e}")

def make_circle_photo(data, size=50):
    """Transforme les bytes image en photo circulaire tkinter."""
    try:
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        # Masque circulaire
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        result = Image.new("RGBA", (size, size), (0,0,0,0))
        result.paste(img, mask=mask)
        return ImageTk.PhotoImage(result)
    except:
        return None

def afficher_photo_header():
    """Affiche la photo dans le header."""
    aid = db.SESSION.get("avocat_id")
    rows = db.query("SELECT photo FROM avocat WHERE id_avocat=%s", (aid,), fetch=True)
    if rows and rows[0][0]:
        photo = make_circle_photo(bytes(rows[0][0]), size=44)
        if photo:
            lbl_photo.config(image=photo, text="")
            lbl_photo.image = photo  # garder référence
    else:
        lbl_photo.config(text="👤", image="", font=("Segoe UI", 22))

# ── Changer mot de passe ──
def changer_mdp():
    aid = db.SESSION.get("avocat_id")
    win = tk.Toplevel(root)
    win.title("Changer mot de passe")
    win.geometry("400x280")
    win.configure(bg=T.BG)
    win.grab_set()

    tk.Label(win, text="🔒 Changer le mot de passe", bg=T.BG, fg=T.CYAN,
             font=("Segoe UI", 13, "bold")).pack(pady=(20,16))
    tk.Label(win, text="Ancien mot de passe :", bg=T.BG, fg=T.TEXT2,
             font=("Segoe UI", 10)).pack(anchor="w", padx=30)
    e_ancien = T.entry(win, w=36, show="•")
    e_ancien.pack(padx=30, pady=(2,10), ipady=6, fill="x")
    tk.Label(win, text="Nouveau mot de passe :", bg=T.BG, fg=T.TEXT2,
             font=("Segoe UI", 10)).pack(anchor="w", padx=30)
    e_nouveau = T.entry(win, w=36, show="•")
    e_nouveau.pack(padx=30, pady=(2,10), ipady=6, fill="x")
    tk.Label(win, text="Confirmer :", bg=T.BG, fg=T.TEXT2,
             font=("Segoe UI", 10)).pack(anchor="w", padx=30)
    e_confirm = T.entry(win, w=36, show="•")
    e_confirm.pack(padx=30, pady=(2,14), ipady=6, fill="x")

    def valider():
        ancien  = e_ancien.get().strip()
        nouveau = e_nouveau.get().strip()
        confirm = e_confirm.get().strip()
        rows = db.query(
            "SELECT id_avocat FROM avocat WHERE id_avocat=%s AND password=%s",
            (aid, ancien), fetch=True)
        if not rows:
            messagebox.showerror("Erreur", "Ancien mot de passe incorrect."); return
        if nouveau != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas."); return
        if not nouveau:
            messagebox.showerror("Erreur", "Mot de passe vide."); return
        db.query("UPDATE avocat SET password=%s WHERE id_avocat=%s", (nouveau, aid))
        messagebox.showinfo("Succès", "Mot de passe changé !")
        win.destroy()

    tk.Button(win, text="✔ Confirmer", command=valider,
              bg=T.CYAN, fg=T.BG, font=("Segoe UI", 10, "bold"),
              relief="flat", padx=18, pady=6, cursor="hand2").pack()

# ── Notes ──
def ouvrir_notes():
    aid = db.SESSION.get("avocat_id")
    win = tk.Toplevel(root)
    win.title("📝 Notes rapides")
    win.geometry("500x400")
    win.configure(bg=T.BG)
    win.grab_set()

    tk.Label(win, text="📝 Mes notes", bg=T.BG, fg=T.CYAN,
             font=("Segoe UI", 13, "bold")).pack(pady=(16,8))

    rows = db.query("SELECT notes FROM avocat WHERE id_avocat=%s", (aid,), fetch=True)
    notes_existantes = rows[0][0] if rows and rows[0][0] else ""

    txt = tk.Text(win, bg=T.BG2, fg=T.TEXT, font=("Segoe UI", 11),
                  relief="flat", insertbackground=T.CYAN,
                  highlightbackground=T.BORDER, highlightthickness=1)
    txt.pack(fill="both", expand=True, padx=16, pady=(0,10))
    txt.insert("1.0", notes_existantes)

    def sauver():
        contenu = txt.get("1.0", "end").strip()
        db.query("UPDATE avocat SET notes=%s WHERE id_avocat=%s", (contenu, aid))
        messagebox.showinfo("Sauvegardé", "Notes sauvegardées !")
        win.destroy()

    tk.Button(win, text="💾 Sauvegarder", command=sauver,
              bg=T.CYAN, fg=T.BG, font=("Segoe UI", 10, "bold"),
              relief="flat", padx=18, pady=6, cursor="hand2").pack(pady=(0,14))

# ── Photo profil ──
def changer_photo():
    aid = db.SESSION.get("avocat_id")
    path = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
    if path:
        with open(path, "rb") as f: data = f.read()
        db.query("UPDATE avocat SET photo=%s WHERE id_avocat=%s", (data, aid))
        messagebox.showinfo("Succès", "Photo de profil mise à jour !")
        afficher_photo_header()  # ← Mise à jour immédiate dans le header

# ── INIT ──
db.init_db()
migration_colonnes()

root = tk.Tk()
root.title("CaseCraft — Tableau de bord")
root.state("zoomed")
T.apply_base(root)

avocat_nom = db.SESSION.get("avocat_nom", "")

# ── Header personnalisé avec photo ──
header = tk.Frame(root, bg=T.BG3, height=58)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="⚖  CaseCraft", bg=T.BG3, fg=T.CYAN,
         font=("Segoe UI", 15, "bold")).pack(side="left", padx=18)
tk.Label(header, text=f"/ Tableau de bord", bg=T.BG3, fg=T.TEXT2,
         font=("Segoe UI", 11)).pack(side="left")
dat = datetime.datetime.now()
tk.Label(header, text="{:%d/%m/%Y  %H:%M}".format(dat),
         bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 9)).pack(side="right", padx=18)

# Zone profil à droite
profil_frame = tk.Frame(header, bg=T.BG3)
profil_frame.pack(side="right", padx=12)

lbl_photo = tk.Label(profil_frame, text="👤", bg=T.BG3, fg=T.CYAN,
                     font=("Segoe UI", 22), cursor="hand2")
lbl_photo.pack(side="left", pady=6)
lbl_photo.bind("<Button-1>", lambda e: changer_photo())

tk.Label(profil_frame, text=avocat_nom, bg=T.BG3, fg=T.WHITE,
         font=("Segoe UI", 11, "bold")).pack(side="left", padx=(6,0))

main = tk.Frame(root, bg=T.BG)
main.pack(fill="both", expand=True)

T.make_sidebar(main, [
    ("📁", "Ajouter affaire",      lambda: nav("AjouterAffaire.py")),
    ("🔍", "Consulter affaires",   lambda: nav("Consulter.py")),
    ("👤", "Ajouter client",       lambda: nav("AjouterClient.py")),
    ("💰", "Finances",             lambda: nav("Fainnace.py")),
    ("📅", "Calendrier",           lambda: nav("calendrie.py")),
    ("🗄", "Archives",             lambda: nav("Archive.py")),
    ("📝", "Notes",                ouvrir_notes),
    ("🔒", "Changer mot de passe", changer_mdp),
    ("🚪", "Déconnexion",          deconnexion),
])

content = tk.Frame(main, bg=T.BG)
content.pack(fill="both", expand=True, padx=20, pady=16)

# ── Stats ligne 1 ──
stats_row = tk.Frame(content, bg=T.BG)
stats_row.pack(fill="x", pady=(0, 8))

def stat_card(parent, icon, label, value, color):
    c = T.card(parent, padx=18, pady=14)
    c.pack(side="left", padx=6, expand=True, fill="x")
    tk.Label(c, text=icon,       bg=T.BG2, fg=color,  font=("Segoe UI", 22)).pack(anchor="w")
    tk.Label(c, text=str(value), bg=T.BG2, fg=T.WHITE, font=("Segoe UI", 20, "bold")).pack(anchor="w")
    tk.Label(c, text=label,      bg=T.BG2, fg=T.TEXT2, font=("Segoe UI", 10)).pack(anchor="w")

stat_card(stats_row, "⚖",  "Mes affaires",     count("affaire"), T.CYAN)
stat_card(stats_row, "🏆", "Affaires gagnées", count_gagnees(),  T.SUCCESS)
stat_card(stats_row, "👥", "Mes clients",       count("client"),  T.ACCENT2)
stat_card(stats_row, "🗄", "Archives",          count("archive"), "#F39C12")

# ── Stats ligne 2 ──
stats_row2 = tk.Frame(content, bg=T.BG)
stats_row2.pack(fill="x", pady=(0, 10))
total, paye, restant = montant_total()
stat_card(stats_row2, "💰", "Montant total (DA)",    f"{total or 0:,.0f}",   T.CYAN)
stat_card(stats_row2, "✅", "Montant encaissé (DA)", f"{paye or 0:,.0f}",    T.SUCCESS)
stat_card(stats_row2, "⏳", "Montant restant (DA)",  f"{restant or 0:,.0f}", T.ACCENT2)

# ── Recherche ──
search_frame = T.card(content, padx=12, pady=10)
search_frame.pack(fill="x", pady=(0, 8))
tk.Label(search_frame, text="🔍", bg=T.BG2, fg=T.CYAN,
         font=("Segoe UI", 13)).pack(side="left", padx=(0, 8))
e_search = T.entry(search_frame, w=60)
e_search.pack(side="left", fill="x", expand=True, ipady=6)
e_search.bind("<Return>", rechercher)
T.btn(search_frame, "Rechercher",  cmd=rechercher,       w=14).pack(side="left", padx=8)
T.btn(search_frame, "Actualiser",  cmd=charger_affaires, w=14, color=T.BG3, hover=T.BORDER, fg=T.TEXT).pack(side="left")
T.btn(search_frame, "🔔 Alertes", cmd=verifier_alertes, w=14, color=T.BG3, hover=T.BORDER, fg=T.CYAN).pack(side="left", padx=4)

# ── Tableau ──
T.style_treeview(None)
cols = (1,2,3,4,5,6,7,8,9,10,11)
tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=12)
headers = ["ID","Autorité","Salle/Dép.","Type client","Nom client",
           "Adversaire","Type affaire","Date dépôt","Décision","Date report","Cause"]
widths  = [40, 120, 100, 100, 120, 120, 110, 100, 110, 100, 120]
for i, (h, w) in enumerate(zip(headers, widths), 1):
    tree.heading(i, text=h); tree.column(i, width=w, anchor="center")

sb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side="left", fill="both", expand=True)
sb.pack(side="left", fill="y")

# Charger la photo au démarrage
afficher_photo_header()
charger_affaires()
verifier_alertes()
root.mainloop()