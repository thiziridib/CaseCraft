# ============================================================
#  main.py — Point d'entrée unique CaseCraft
#  Navigation par frames (pas de subprocess)
# ============================================================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import datetime
import os, sys
import theme as T
import db
from PIL import Image, ImageTk, ImageDraw
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import date as dt_date

# ============================================================
#  TRADUCTIONS FR / AR
# ============================================================
LANGUE = {"actuelle": "FR"}

TRADUCTIONS = {
    "FR": {
        "bienvenue": "Bienvenue",
        "connectez": "Connectez-vous à votre espace",
        "utilisateur": "Nom d'utilisateur",
        "mdp": "Mot de passe",
        "se_connecter": "Se connecter",
        "pas_compte": "Pas de compte ?",
        "sinscrire": "  S'inscrire",
        "inscription": "Inscription",
        "nom": "Nom",
        "numero": "Numéro",
        "creer": "Créer le compte",
        "deja_compte": "Déjà un compte ?",
        "se_connecter2": "  Se connecter",
        "tableau_bord": "Tableau de bord",
        "ajouter_affaire": "Ajouter affaire",
        "consulter": "Consulter",
        "clients": "Clients",
        "finances": "Finances",
        "calendrier": "Calendrier",
        "archives": "Archives",
        "notes": "Notes",
        "changer_mdp": "Changer mot de passe",
        "photo": "Photo profil",
        "deconnexion": "Déconnexion",
        "mes_affaires": "Mes affaires",
        "affaires_gagnees": "Affaires gagnées",
        "mes_clients": "Mes clients",
        "montant_total": "Montant total (DA)",
        "montant_encaisse": "Montant encaissé (DA)",
        "montant_restant": "Montant restant (DA)",
        "rechercher": "Rechercher",
        "actualiser": "Actualiser",
        "alertes": "🔔 Alertes",
        "nouvelle_affaire": "Nouvelle affaire",
        "nom_client": "Nom du client",
        "adversaire": "Adversaire",
        "autorite": "Autorité judiciaire",
        "departement": "Département / Salle",
        "type_client": "Type de client",
        "type_affaire": "Type d'affaire",
        "frais": "Frais d'affaire (DA)",
        "enquete": "Numéro d'enquête",
        "date_depot": "Date de dépôt (AAAA-MM-JJ)",
        "decision": "Décision finale",
        "date_report": "Date de report",
        "cause": "Cause de report",
        "sujet": "Sujet",
        "remarque": "Remarque",
        "enregistrer": "✔ Enregistrer l'affaire",
        "annuler": "✖ Annuler",
        "ajouter": "➕ Ajouter",
        "modifier": "✏ Modifier",
        "supprimer": "🗑 Supprimer",
        "archiver": "🗄 Archiver",
        "pdf": "📄 PDF",
        "joindre": "📎 Joindre",
        "nouveau_paiement": "Nouveau paiement",
        "nom_client2": "Nom client",
        "montant_payer": "Montant à payer",
        "montant_paye": "Montant payé",
        "date_paiement": "Date (AAAA-MM-JJ)",
        "montant_auto": "Montant restant (auto)",
        "enregistrer2": "➕ Enregistrer",
        "export_pdf": "📄 PDF",
        "filtrer": "🔍 Filtrer",
        "fermer": "✖ Fermer",
        "details": "Détails & Modification",
        "remporter": "🏆 Remporter affaire",
        "saisir_dec": "⚖️ Décision",
        "info_generales": "Informations générales",
        "info_client": "Informations client",
        "sujet_remarques": "Sujet & Remarques",
        "id": "ID",
        "nom_col": "Nom",
        "prenom": "Prénom",
        "adresse": "Adresse",
        "email": "Email",
        "telephone": "Téléphone",
        "document": "Document",
        "autorite_col": "Autorité",
        "salle": "Salle",
        "type_client_col": "Type client",
        "nom_client_col": "Nom client",
        "adversaire_col": "Adversaire",
        "type_affaire_col": "Type affaire",
        "date_depot_col": "Date dépôt",
        "decision_col": "Décision",
        "date_report_col": "Date report",
        "cause_col": "Cause",
        "montant_col": "Montant",
        "paye_col": "Payé",
        "restant_col": "Restant",
        "date_col": "Date",
        "dept_col": "Dép.",
        "sujet_col": "Sujet",
        "remarque_col": "Remarque",
        "frais_col": "Frais",
        "enquete_col": "N° enquête",
    },
    "AR": {
        "bienvenue": "مرحباً",
        "connectez": "سجّل دخولك إلى حسابك",
        "utilisateur": "اسم المستخدم",
        "mdp": "كلمة المرور",
        "se_connecter": "تسجيل الدخول",
        "pas_compte": "ليس لديك حساب ؟",
        "sinscrire": "  إنشاء حساب",
        "inscription": "إنشاء حساب",
        "nom": "الاسم",
        "numero": "الرقم",
        "creer": "إنشاء الحساب",
        "deja_compte": "لديك حساب بالفعل ؟",
        "se_connecter2": "  تسجيل الدخول",
        "tableau_bord": "لوحة التحكم",
        "ajouter_affaire": "إضافة قضية",
        "consulter": "استعراض",
        "clients": "الموكلون",
        "finances": "المالية",
        "calendrier": "الجدول الزمني",
        "archives": "الأرشيف",
        "notes": "الملاحظات",
        "changer_mdp": "تغيير كلمة المرور",
        "photo": "صورة الملف الشخصي",
        "deconnexion": "تسجيل الخروج",
        "mes_affaires": "قضاياي",
        "affaires_gagnees": "القضايا المكسوبة",
        "mes_clients": "موكلوني",
        "montant_total": "المبلغ الإجمالي (دج)",
        "montant_encaisse": "المبلغ المحصّل (دج)",
        "montant_restant": "المبلغ المتبقي (دج)",
        "rechercher": "بحث",
        "actualiser": "تحديث",
        "alertes": "🔔 التنبيهات",
        "nouvelle_affaire": "قضية جديدة",
        "nom_client": "اسم الموكل",
        "adversaire": "الخصم",
        "autorite": "الجهة القضائية",
        "departement": "القسم / القاعة",
        "type_client": "نوع الموكل",
        "type_affaire": "نوع القضية",
        "frais": "أتعاب القضية (دج)",
        "enquete": "رقم التحقيق",
        "date_depot": "تاريخ الإيداع (AAAA-MM-JJ)",
        "decision": "القرار النهائي",
        "date_report": "تاريخ التأجيل",
        "cause": "سبب التأجيل",
        "sujet": "الموضوع",
        "remarque": "ملاحظة",
        "enregistrer": "✔ حفظ القضية",
        "annuler": "✖ إلغاء",
        "ajouter": "➕ إضافة",
        "modifier": "✏ تعديل",
        "supprimer": "🗑 حذف",
        "archiver": "🗄 أرشفة",
        "pdf": "📄 PDF",
        "joindre": "📎 إرفاق",
        "nouveau_paiement": "دفعة جديدة",
        "nom_client2": "اسم الموكل",
        "montant_payer": "المبلغ المستحق",
        "montant_paye": "المبلغ المدفوع",
        "date_paiement": "تاريخ الدفع",
        "montant_auto": "المبلغ المتبقي (تلقائي)",
        "enregistrer2": "➕ تسجيل",
        "export_pdf": "📄 PDF",
        "filtrer": "🔍 تصفية",
        "fermer": "✖ إغلاق",
        "details": "التفاصيل والتعديل",
        "remporter": "🏆 ربح القضية",
        "saisir_dec": "⚖️ القرار",
        "info_generales": "معلومات عامة",
        "info_client": "معلومات الموكل",
        "sujet_remarques": "الموضوع والملاحظات",
        "id": "المعرف",
        "nom_col": "الاسم",
        "prenom": "اللقب",
        "adresse": "العنوان",
        "email": "البريد الإلكتروني",
        "telephone": "الهاتف",
        "document": "وثيقة",
        "autorite_col": "الجهة القضائية",
        "salle": "القاعة",
        "type_client_col": "نوع الموكل",
        "nom_client_col": "اسم الموكل",
        "adversaire_col": "الخصم",
        "type_affaire_col": "نوع القضية",
        "date_depot_col": "تاريخ الإيداع",
        "decision_col": "القرار",
        "date_report_col": "تاريخ التأجيل",
        "cause_col": "السبب",
        "montant_col": "المبلغ",
        "paye_col": "المدفوع",
        "restant_col": "المتبقي",
        "date_col": "التاريخ",
        "dept_col": "القسم",
        "sujet_col": "الموضوع",
        "remarque_col": "ملاحظة",
        "frais_col": "الأتعاب",
        "enquete_col": "رقم التحقيق",
    }
}

def T_(key):
    """Retourne la traduction selon la langue actuelle."""
    return TRADUCTIONS[LANGUE["actuelle"]].get(key, key)

# Page courante affichée
PAGE_ACTIVE = {"nom": "splash"}

def toggle_langue(btn=None):
    """Bascule entre FR et AR et reconstruit toutes les pages."""
    LANGUE["actuelle"] = "AR" if LANGUE["actuelle"] == "FR" else "FR"
    nom = PAGE_ACTIVE.get("nom", "dashboard")

    # Reconstruire toutes les pages proprement
    for name, page in list(pages.items()):
        if name in ("splash",): continue
        try:
            # Détruire tous les widgets enfants
            for w in page.winfo_children():
                w.destroy()
            # Recréer frame+content pour les pages avec make_page_frame
            if hasattr(page, "_titres") and hasattr(page, "_page_active_key"):
                page.frame, page.content = make_page_frame(
                    page, page._titres[LANGUE["actuelle"]], page._page_active_key)
                page.frame.pack(fill="both", expand=True)
                page._build()
            elif hasattr(page, "_build"):
                page._build()
        except Exception as e:
            print(f"Rebuild {name}: {e}")

    show_page(nom)


# ============================================================
#  APP PRINCIPALE
# ============================================================
db.init_db()

# Migration colonnes notes/photo
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
        cx.commit(); cx.close()
    except Exception as e:
        print(f"Migration: {e}")

migration_colonnes()

root = tk.Tk()
root.title("CaseCraft")
root.state("zoomed")
root.configure(bg=T.BG)

# Container principal qui contient toutes les pages
container = tk.Frame(root, bg=T.BG)
container.pack(fill="both", expand=True)

# ============================================================
#  NAVIGATION — affiche une page, cache les autres
# ============================================================
pages = {}

def show_page(name):
    PAGE_ACTIVE["nom"] = name
    for p in pages.values():
        p.pack_forget()
    pages[name].pack(fill="both", expand=True)
    if hasattr(pages[name], "on_show"):
        pages[name].on_show()

# ============================================================
#  SPLASH SCREEN
# ============================================================
class SplashPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0D1B2A")
        tk.Label(self, text="⚖", bg="#0D1B2A", fg="#1ABC9C",
                 font=("Segoe UI", 52)).pack(pady=(80, 8))
        tk.Label(self, text="CaseCraft", bg="#0D1B2A", fg="white",
                 font=("Segoe UI", 28, "bold")).pack()
        tk.Label(self, text="Gestion Cabinet d'Avocat", bg="#0D1B2A", fg="#95A5A6",
                 font=("Segoe UI", 11)).pack(pady=4)
        self.lbl = tk.Label(self, text="Chargement... 0%", bg="#0D1B2A", fg="#95A5A6",
                            font=("Segoe UI", 10))
        self.lbl.pack(pady=(24, 6))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Green.Horizontal.TProgressbar",
                        troughcolor="#162032", background="#1ABC9C", borderwidth=0)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=340,
                                        mode="determinate",
                                        style="Green.Horizontal.TProgressbar")
        self.progress.pack()
        self.i = 0
        self.after(300, self.load)

    def load(self):
        if self.i <= 10:
            self.lbl.config(text=f"Chargement... {self.i*10}%")
            self.progress["value"] = self.i * 10
            self.i += 1
            self.after(300, self.load)
        else:
            show_page("login")

# ============================================================
#  PAGE LOGIN
# ============================================================
class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._build()

    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=T.BG3, width=360)
        left.pack(fill="y", side="left")
        left.pack_propagate(False)
        tk.Label(left, text="⚖", bg=T.BG3, fg=T.CYAN, font=("Segoe UI", 60)).pack(pady=(80,10))
        tk.Label(left, text="CaseCraft", bg=T.BG3, fg=T.WHITE, font=("Segoe UI", 28, "bold")).pack()
        tk.Label(left, text="Gestion Cabinet d'Avocat", bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 11)).pack(pady=4)
        tk.Frame(left, bg=T.BORDER, height=1, width=200).pack(pady=20)
        tk.Label(left, text='"La justice est le fondement\nde toute société équitable."',
                 bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 10, "italic"), justify="center").pack(padx=20)

        right = tk.Frame(self, bg=T.BG)
        right.pack(fill="both", expand=True)
        form = T.card(right, padx=40, pady=40)
        form.place(relx=0.5, rely=0.5, anchor="center", width=400, height=430)

        T.lbl(form, T_("bienvenue"), size=18, bold=True, color=T.WHITE, bg=T.BG2).pack(pady=(0,4))
        T.lbl(form, T_("connectez"), size=10, color=T.TEXT2, bg=T.BG2).pack(pady=(0,20))
        T.lbl(form, T_("utilisateur"), size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        self.e_nom = T.entry(form, w=32)
        self.e_nom.pack(fill="x", pady=(4,14), ipady=7)
        T.lbl(form, T_("mdp"), size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        self.e_mdp = T.entry(form, w=32, show="•")
        self.e_mdp.pack(fill="x", pady=(4,20), ipady=7)
        self.e_mdp.bind("<Return>", lambda e: self.valider())
        T.btn(form, T_("se_connecter"), cmd=self.valider, w=32).pack(fill="x", ipady=4)

        link_frame = tk.Frame(form, bg=T.BG2); link_frame.pack(pady=(14,0))
        T.lbl(link_frame, "Pas de compte ?", size=9, color=T.TEXT2, bg=T.BG2).pack(side="left")
        lnk = T.lbl(link_frame, "  S'inscrire", size=9, bold=True, color=T.CYAN, bg=T.BG2)
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: show_page("inscription"))
        lnk.config(cursor="hand2")

    def valider(self):
        nom = self.e_nom.get().strip()
        mdp = self.e_mdp.get().strip()
        if not nom or not mdp:
            messagebox.showwarning("Champs vides", "Remplissez tous les champs."); return
        rows = db.query("SELECT id_avocat, nom FROM avocat WHERE nom=%s AND password=%s",
                        (nom, mdp), fetch=True)
        if rows:
            db.SESSION["avocat_id"]  = rows[0][0]
            db.SESSION["avocat_nom"] = rows[0][1]
            db.sauver_session()
            self.e_nom.delete(0, "end")
            self.e_mdp.delete(0, "end")
            show_page("dashboard")
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects.")

# ============================================================
#  PAGE INSCRIPTION
# ============================================================
class InscriptionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._build()

    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=T.BG3, width=360)
        left.pack(fill="y", side="left"); left.pack_propagate(False)
        tk.Label(left, text="⚖", bg=T.BG3, fg=T.CYAN, font=("Segoe UI", 60)).pack(pady=(80,10))
        tk.Label(left, text="CaseCraft", bg=T.BG3, fg=T.WHITE, font=("Segoe UI", 28, "bold")).pack()
        tk.Label(left, text="Créer un compte avocat", bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 11)).pack(pady=4)

        right = tk.Frame(self, bg=T.BG); right.pack(fill="both", expand=True)
        form = T.card(right, padx=40, pady=40)
        form.place(relx=0.5, rely=0.5, anchor="center", width=380, height=420)

        T.lbl(form, "Inscription", size=18, bold=True, color=T.WHITE, bg=T.BG2).pack(pady=(0,20))
        T.lbl(form, "Nom", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        self.e_nom = T.entry(form, w=32); self.e_nom.pack(fill="x", pady=(4,12), ipady=7)
        T.lbl(form, "Numéro", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        self.e_num = T.entry(form, w=32); self.e_num.pack(fill="x", pady=(4,12), ipady=7)
        T.lbl(form, "Mot de passe", size=10, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        self.e_mdp = T.entry(form, w=32, show="•"); self.e_mdp.pack(fill="x", pady=(4,20), ipady=7)
        T.btn(form, "Créer le compte", cmd=self.valider, w=32).pack(fill="x", ipady=4)

        link_frame = tk.Frame(form, bg=T.BG2); link_frame.pack(pady=(12,0))
        T.lbl(link_frame, "Déjà un compte ?", size=9, color=T.TEXT2, bg=T.BG2).pack(side="left")
        lnk = T.lbl(link_frame, "  Se connecter", size=9, bold=True, color=T.CYAN, bg=T.BG2)
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: show_page("login"))
        lnk.config(cursor="hand2")

    def valider(self):
        nom = self.e_nom.get().strip()
        num = self.e_num.get().strip()
        mdp = self.e_mdp.get().strip()
        if not all([nom, num, mdp]):
            messagebox.showwarning("Champs vides", "Remplissez tous les champs."); return
        if not num.isdigit():
            messagebox.showerror("Erreur", "Le numéro doit contenir uniquement des chiffres."); return
        existe = db.query("SELECT id_avocat FROM avocat WHERE nom=%s", (nom,), fetch=True)
        if existe:
            messagebox.showerror("Erreur", "Ce nom existe déjà."); return
        ok = db.query("INSERT INTO avocat (nom,numero,password) VALUES (%s,%s,%s)", (nom,num,mdp))
        if ok:
            messagebox.showinfo("Succès", "Inscription réussie ! Connectez-vous.")
            self.e_nom.delete(0,"end"); self.e_num.delete(0,"end"); self.e_mdp.delete(0,"end")
            show_page("login")

# ============================================================
#  HELPER — cadre de page avec header + sidebar
# ============================================================
def make_page_frame(parent, titre, page_active):
    frame = tk.Frame(parent, bg=T.BG)

    # Header
    hdr = tk.Frame(frame, bg=T.BG3, height=58)
    hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Label(hdr, text="⚖  CaseCraft", bg=T.BG3, fg=T.CYAN,
             font=("Segoe UI", 15, "bold")).pack(side="left", padx=18)
    tk.Label(hdr, text=f"/ {titre}", bg=T.BG3, fg=T.TEXT2,
             font=("Segoe UI", 11)).pack(side="left")
    tk.Label(hdr, text="{:%d/%m/%Y  %H:%M}".format(datetime.datetime.now()),
             bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 9)).pack(side="right", padx=18)

    # Bouton FR/AR
    btn_lang = tk.Button(hdr, text="🌐 AR" if LANGUE["actuelle"] == "FR" else "🌐 FR",
                  bg=T.BORDER, fg=T.CYAN,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=10, pady=3, cursor="hand2")
    btn_lang.config(command=lambda: toggle_langue())
    btn_lang.pack(side="right", padx=6, pady=12)

    # Body
    body = tk.Frame(frame, bg=T.BG)
    body.pack(fill="both", expand=True)

    # Sidebar
    nav_items = [
        ("📁", T_("ajouter_affaire"), "ajouter_affaire"),
        ("🔍", T_("consulter"),       "consulter"),
        ("👤", T_("clients"),         "clients"),
        ("💰", T_("finances"),        "finances"),
        ("📅", T_("calendrier"),      "calendrier"),
        ("🗄", T_("archives"),        "archives"),
        ("🏠", T_("tableau_bord"),    "dashboard"),
    ]
    sb = tk.Frame(body, bg=T.BG3, width=200)
    sb.pack(fill="y", side="left"); sb.pack_propagate(False)
    tk.Label(sb, text="NAVIGATION", bg=T.BG3, fg=T.TEXT2,
             font=("Segoe UI", 8, "bold")).pack(pady=(18,6), padx=12, anchor="w")
    for icon, label, page in nav_items:
        r = tk.Frame(sb, bg=T.BG3 if page != page_active else T.BORDER, cursor="hand2")
        r.pack(fill="x", pady=1)
        l = tk.Label(r, text=f"  {icon}  {label}", bg=T.BG3 if page != page_active else T.BORDER,
                     fg=T.CYAN if page == page_active else T.TEXT,
                     font=("Segoe UI", 11), anchor="w", pady=9, padx=8)
        l.pack(fill="x")
        for w in (r, l):
            w.bind("<Enter>", lambda e, rr=r, ll=l: (rr.config(bg=T.BORDER), ll.config(bg=T.BORDER)))
            w.bind("<Leave>", lambda e, rr=r, ll=l, pg=page: (
                rr.config(bg=T.BORDER if pg == page_active else T.BG3),
                ll.config(bg=T.BORDER if pg == page_active else T.BG3)))
            w.bind("<Button-1>", lambda e, pg=page: show_page(pg))

    # Content area
    content = tk.Frame(body, bg=T.BG)
    content.pack(fill="both", expand=True, padx=16, pady=14)

    return frame, content

# ============================================================
#  DASHBOARD
# ============================================================
class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)

    def _build(self):
        self.on_show()

    def on_show(self):
        for w in self.winfo_children(): w.destroy()
        aid = db.SESSION.get("avocat_id")
        avocat_nom = db.SESSION.get("avocat_nom", "")

        # Header
        hdr = tk.Frame(self, bg=T.BG3, height=58)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="⚖  CaseCraft", bg=T.BG3, fg=T.CYAN,
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=18)
        tk.Label(hdr, text="/ Tableau de bord", bg=T.BG3, fg=T.TEXT2,
                 font=("Segoe UI", 11)).pack(side="left")
        tk.Label(hdr, text="{:%d/%m/%Y  %H:%M}".format(datetime.datetime.now()),
                 bg=T.BG3, fg=T.TEXT2, font=("Segoe UI", 9)).pack(side="right", padx=18)

        # Bouton FR/AR
        self._btn_lang = tk.Button(hdr, text="🌐 AR", bg=T.BORDER, fg=T.CYAN,
                      font=("Segoe UI", 10, "bold"), relief="flat",
                      padx=10, pady=3, cursor="hand2",
                      command=lambda: toggle_langue())
        self._btn_lang.pack(side="right", padx=6, pady=12)

        # Photo profil dans header
        pf = tk.Frame(hdr, bg=T.BG3); pf.pack(side="right", padx=12)
        rows = db.query("SELECT photo FROM avocat WHERE id_avocat=%s", (aid,), fetch=True)
        if rows and rows[0][0]:
            try:
                img = Image.open(io.BytesIO(bytes(rows[0][0]))).convert("RGBA")
                img = img.resize((44,44), Image.LANCZOS)
                mask = Image.new("L",(44,44),0)
                ImageDraw.Draw(mask).ellipse((0,0,44,44),fill=255)
                result = Image.new("RGBA",(44,44),(0,0,0,0))
                result.paste(img, mask=mask)
                self._photo = ImageTk.PhotoImage(result)
                tk.Label(pf, image=self._photo, bg=T.BG3).pack(side="left", pady=7)
            except: tk.Label(pf, text="👤", bg=T.BG3, fg=T.CYAN, font=("Segoe UI",22)).pack(side="left")
        else:
            tk.Label(pf, text="👤", bg=T.BG3, fg=T.CYAN, font=("Segoe UI",22)).pack(side="left")
        tk.Label(pf, text=avocat_nom, bg=T.BG3, fg=T.WHITE,
                 font=("Segoe UI",11,"bold")).pack(side="left", padx=(6,0))

        body = tk.Frame(self, bg=T.BG); body.pack(fill="both", expand=True)

        # Sidebar
        sb = tk.Frame(body, bg=T.BG3, width=200)
        sb.pack(fill="y", side="left"); sb.pack_propagate(False)
        tk.Label(sb, text="NAVIGATION", bg=T.BG3, fg=T.TEXT2,
                 font=("Segoe UI",8,"bold")).pack(pady=(18,6), padx=12, anchor="w")
        nav_items = [
            ("📁",T_("ajouter_affaire"),"ajouter_affaire"),
            ("🔍",T_("consulter"),"consulter"),
            ("👤",T_("clients"),"clients"),
            ("💰",T_("finances"),"finances"),
            ("📅",T_("calendrier"),"calendrier"),
            ("🗄",T_("archives"),"archives"),
            ("📝",T_("notes"), None),
            ("🔒",T_("changer_mdp"), None),
            ("🖼",T_("photo"), None),
            ("🚪",T_("deconnexion"), None),
        ]
        def deconnexion():
            if messagebox.askyesno("Déconnexion","Voulez-vous vous déconnecter ?"):
                db.effacer_session(); show_page("login")
        def ouvrir_notes():
            win = tk.Toplevel(root); win.title("Notes"); win.geometry("500x400")
            win.configure(bg=T.BG); win.grab_set()
            tk.Label(win, text="📝 Mes notes", bg=T.BG, fg=T.CYAN,
                     font=("Segoe UI",13,"bold")).pack(pady=(16,8))
            rows = db.query("SELECT notes FROM avocat WHERE id_avocat=%s",(aid,),fetch=True)
            txt = tk.Text(win, bg=T.BG2, fg=T.TEXT, font=("Segoe UI",11),
                          relief="flat", insertbackground=T.CYAN,
                          highlightbackground=T.BORDER, highlightthickness=1)
            txt.pack(fill="both", expand=True, padx=16, pady=(0,10))
            txt.insert("1.0", rows[0][0] if rows and rows[0][0] else "")
            def sauver():
                db.query("UPDATE avocat SET notes=%s WHERE id_avocat=%s",(txt.get("1.0","end").strip(),aid))
                messagebox.showinfo("OK","Notes sauvegardées !"); win.destroy()
            tk.Button(win, text="💾 Sauvegarder", command=sauver, bg=T.CYAN, fg=T.BG,
                      font=("Segoe UI",10,"bold"), relief="flat", padx=18, pady=6,
                      cursor="hand2").pack(pady=(0,14))
        def changer_mdp():
            win = tk.Toplevel(root); win.title("Mot de passe"); win.geometry("400x280")
            win.configure(bg=T.BG); win.grab_set()
            tk.Label(win, text="🔒 Changer le mot de passe", bg=T.BG, fg=T.CYAN,
                     font=("Segoe UI",13,"bold")).pack(pady=(20,16))
            for lbl_txt, attr, show in [("Ancien :","e_a","•"),("Nouveau :","e_n","•"),("Confirmer :","e_c","•")]:
                tk.Label(win, text=lbl_txt, bg=T.BG, fg=T.TEXT2, font=("Segoe UI",10)).pack(anchor="w",padx=30)
                e = T.entry(win, w=36, show=show); e.pack(padx=30, pady=(2,10), ipady=6, fill="x")
                setattr(win, attr, e)
            def valider():
                r = db.query("SELECT id_avocat FROM avocat WHERE id_avocat=%s AND password=%s",
                             (aid, win.e_a.get()), fetch=True)
                if not r: messagebox.showerror("Erreur","Ancien MDP incorrect."); return
                if win.e_n.get() != win.e_c.get(): messagebox.showerror("Erreur","MDP différents."); return
                db.query("UPDATE avocat SET password=%s WHERE id_avocat=%s",(win.e_n.get(),aid))
                messagebox.showinfo("OK","Mot de passe changé !"); win.destroy()
            tk.Button(win, text="✔ Confirmer", command=valider, bg=T.CYAN, fg=T.BG,
                      font=("Segoe UI",10,"bold"), relief="flat", padx=18, pady=6, cursor="hand2").pack()
        def changer_photo():
            path = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
            if path:
                with open(path,"rb") as f: data = f.read()
                db.query("UPDATE avocat SET photo=%s WHERE id_avocat=%s",(data,aid))
                messagebox.showinfo("Succès","Photo mise à jour !")
                self.on_show()

        actions = {"📝 Notes": ouvrir_notes, "🔒 Changer mot de passe": changer_mdp,
                   "🖼 Photo profil": changer_photo, "🚪 Déconnexion": deconnexion}
        for icon, label, page in nav_items:
            r = tk.Frame(sb, bg=T.BG3, cursor="hand2"); r.pack(fill="x", pady=1)
            l = tk.Label(r, text=f"  {icon}  {label}", bg=T.BG3, fg=T.TEXT,
                         font=("Segoe UI",11), anchor="w", pady=9, padx=8); l.pack(fill="x")
            cmd = (lambda pg=page: show_page(pg)) if page else actions.get(f"{icon} {label}", lambda:None)
            for w in (r,l):
                w.bind("<Enter>", lambda e,rr=r,ll=l:(rr.config(bg=T.BORDER),ll.config(bg=T.BORDER)))
                w.bind("<Leave>", lambda e,rr=r,ll=l:(rr.config(bg=T.BG3),ll.config(bg=T.BG3)))
                w.bind("<Button-1>", lambda e,c=cmd:c())

        content = tk.Frame(body, bg=T.BG); content.pack(fill="both", expand=True, padx=20, pady=16)

        def count(table):
            r = db.query(f"SELECT COUNT(*) FROM {table} WHERE avocat_id=%s",(aid,),fetch=True)
            return r[0][0] if r else 0
        def count_gagnees():
            r = db.query("SELECT COUNT(*) FROM affaire WHERE avocat_id=%s AND decision_finale='Gagnée'",(aid,),fetch=True)
            return r[0][0] if r else 0
        def montant_total():
            r = db.query("SELECT SUM(montant),SUM(montant_payee),SUM(montant_restant) FROM financement WHERE avocat_id=%s",(aid,),fetch=True)
            return r[0] if r and r[0][0] else (0,0,0)

        def stat_card(parent, icon, label, value, color):
            c = T.card(parent, padx=18, pady=14); c.pack(side="left", padx=6, expand=True, fill="x")
            tk.Label(c, text=icon, bg=T.BG2, fg=color, font=("Segoe UI",22)).pack(anchor="w")
            tk.Label(c, text=str(value), bg=T.BG2, fg=T.WHITE, font=("Segoe UI",20,"bold")).pack(anchor="w")
            tk.Label(c, text=label, bg=T.BG2, fg=T.TEXT2, font=("Segoe UI",10)).pack(anchor="w")

        r1 = tk.Frame(content, bg=T.BG); r1.pack(fill="x", pady=(0,8))
        stat_card(r1,"⚖",T_("mes_affaires"),count("affaire"),T.CYAN)
        stat_card(r1,"🏆",T_("affaires_gagnees"),count_gagnees(),T.SUCCESS)
        stat_card(r1,"👥",T_("mes_clients"),count("client"),T.ACCENT2)
        stat_card(r1,"🗄",T_("archives"),count("archive"),"#F39C12")

        r2 = tk.Frame(content, bg=T.BG); r2.pack(fill="x", pady=(0,10))
        total,paye,restant = montant_total()
        stat_card(r2,"💰",T_("montant_total"),f"{total or 0:,.0f}",T.CYAN)
        stat_card(r2,"✅",T_("montant_encaisse"),f"{paye or 0:,.0f}",T.SUCCESS)
        stat_card(r2,"⏳",T_("montant_restant"),f"{restant or 0:,.0f}",T.ACCENT2)

        # Recherche
        sf = T.card(content, padx=12, pady=10); sf.pack(fill="x", pady=(0,8))
        tk.Label(sf, text="🔍", bg=T.BG2, fg=T.CYAN, font=("Segoe UI",13)).pack(side="left",padx=(0,8))
        e_search = T.entry(sf, w=60); e_search.pack(side="left", fill="x", expand=True, ipady=6)

        T.style_treeview(None)
        cols = tuple(range(1,12))
        tree = ttk.Treeview(content, columns=cols, show="headings", style="M.Treeview", height=11)
        hdrs = [T_("id"),T_("autorite_col"),T_("salle"),T_("type_client_col"),T_("nom_client_col"),T_("adversaire_col"),T_("type_affaire_col"),T_("date_depot_col"),T_("decision_col"),T_("date_report_col"),T_("cause_col")]
        wds  = [40,120,100,100,120,120,110,100,110,100,120]
        for i,(h,w) in enumerate(zip(hdrs,wds),1):
            tree.heading(i,text=h); tree.column(i,width=w,anchor="center")

        def charger():
            for i in tree.get_children(): tree.delete(i)
            rows = db.query(
                "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
                "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
                "FROM affaire WHERE avocat_id=%s",(aid,),fetch=True)
            for row in rows: tree.insert("","end",values=row)

        def rechercher(event=None):
            terme = e_search.get().strip()
            for i in tree.get_children(): tree.delete(i)
            rows = db.query(
                "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
                "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
                "FROM affaire WHERE avocat_id=%s AND (nom_client LIKE %s OR adversaire LIKE %s OR type_affaire LIKE %s)",
                (aid,f"%{terme}%",f"%{terme}%",f"%{terme}%"),fetch=True)
            for row in rows: tree.insert("","end",values=row)

        e_search.bind("<Return>", rechercher)
        T.btn(sf,"Rechercher",cmd=rechercher,w=14).pack(side="left",padx=8)
        T.btn(sf,"Actualiser",cmd=charger,w=12,color=T.BG3,hover=T.BORDER,fg=T.TEXT).pack(side="left")

        sb2 = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb2.set)
        tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="left", fill="y")
        charger()

        # Alertes
        def verifier_alertes():
            rows = db.query(
                "SELECT nom_client,date_depot_dossier FROM affaire "
                "WHERE avocat_id=%s AND DATEDIFF(date_depot_dossier,CURDATE()) BETWEEN 0 AND 5",
                (aid,),fetch=True)
            if rows:
                msg = "⚠ Audiences dans les 5 prochains jours :\n\n"
                for n,d in rows: msg += f"• {n}  →  {d}\n"
                messagebox.showwarning("Alerte",msg)
        root.after(500, verifier_alertes)

# ============================================================
#  PAGE CONSULTER
# ============================================================
class ConsulterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._parent = parent
        self._titres = {'FR': 'Consulter les affaires', 'AR': 'استعراض القضايا'}
        self._page_active_key = "consulter"
        self.frame, self.content = make_page_frame(self, "Consulter les affaires", "consulter")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _rebuild_frame(self):
        """Reconstruit frame+content pour appliquer la nouvelle langue."""
        for w in self.winfo_children(): w.destroy()
        self.frame, self.content = make_page_frame(self, self._titres[LANGUE["actuelle"]], "consulter")
        self.frame.pack(fill="both", expand=True)
        self._build()
        self.charger()

    def _build(self):
        c = self.content
        aid = lambda: db.SESSION.get("avocat_id")

        toolbar = T.card(c, padx=12, pady=10); toolbar.pack(fill="x", pady=(0,12))
        tk.Label(toolbar, text="🔍", bg=T.BG2, fg=T.CYAN, font=("Segoe UI",13)).pack(side="left",padx=(0,8))
        self.e_search = T.entry(toolbar, w=50)
        self.e_search.pack(side="left", fill="x", expand=True, ipady=6)
        self.e_search.bind("<Return>", lambda e: self.rechercher())
        T.btn(toolbar,T_("rechercher"),cmd=self.rechercher,w=14).pack(side="left",padx=6)
        T.btn(toolbar,T_("actualiser"),cmd=self.charger,w=12,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4)
        T.btn(toolbar,T_("supprimer"),cmd=self.supprimer,w=14,color=T.BG3,hover=T.BORDER,fg=T.ACCENT2).pack(side="left",padx=4)
        T.btn(toolbar,T_("archiver"),cmd=self.archiver,w=14,color=T.BG3,hover=T.BORDER,fg=T.CYAN).pack(side="left",padx=4)
        T.btn(toolbar,T_("pdf"),cmd=self.exporter_pdf,w=10,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4)

        T.style_treeview(None)
        cols = tuple(range(1,12))
        self.tree = ttk.Treeview(c, columns=cols, show="headings", style="M.Treeview", height=20)
        hdrs = [T_("id"),T_("autorite_col"),T_("salle"),T_("type_client_col"),T_("nom_client_col"),T_("adversaire_col"),T_("type_affaire_col"),T_("date_depot_col"),T_("decision_col"),T_("date_report_col"),T_("cause_col")]
        wds  = [40,120,90,100,120,120,110,100,110,100,120]
        for i,(h,w) in enumerate(zip(hdrs,wds),1):
            self.tree.heading(i,text=h); self.tree.column(i,width=w,anchor="center")
        sb = ttk.Scrollbar(c, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")
        self.tree.bind("<Double-1>", self.afficher_details)

    def on_show(self): self.charger()

    def charger(self):
        aid = db.SESSION.get("avocat_id")
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query(
            "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
            "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
            "FROM affaire WHERE avocat_id=%s",(aid,),fetch=True)
        for r in rows: self.tree.insert("","end",values=r)

    def rechercher(self):
        aid = db.SESSION.get("avocat_id"); terme = self.e_search.get().strip()
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query(
            "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
            "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
            "FROM affaire WHERE avocat_id=%s AND (nom_client LIKE %s OR adversaire LIKE %s OR type_affaire LIKE %s)",
            (aid,f"%{terme}%",f"%{terme}%",f"%{terme}%"),fetch=True)
        for r in rows: self.tree.insert("","end",values=r)

    def supprimer(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection","Sélectionnez une affaire."); return
        if messagebox.askyesno("Confirmation","Supprimer cette affaire ?"):
            cid = self.tree.item(sel[0],"values")[0]
            db.query("DELETE FROM affaire WHERE id=%s AND avocat_id=%s",(cid,db.SESSION.get("avocat_id")))
            self.charger()

    def archiver(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection","Sélectionnez une affaire."); return
        cid = self.tree.item(sel[0],"values")[0]
        self.archiver_par_id(cid)

    def archiver_par_id(self, cid, fen=None):
        aid = db.SESSION.get("avocat_id")
        row = db.query("SELECT * FROM affaire WHERE id=%s AND avocat_id=%s",(cid,aid),fetch=True)
        if not row:
            messagebox.showwarning("Erreur","Affaire introuvable."); return
        r = row[0]
        # Structure affaire: id(0),avocat_id(1),autorite(2),salle(3),type_client(4),
        # nom_client(5),sujet(6),adversaire(7),remarque(8),frais(9),type_affaire(10),
        # numero_enquete(11),date_depot(12),decision_finale(13),date(14),cause(15)
        try:
            # Nettoyer la date de dépôt
            date_depot = r[12]
            if date_depot and str(date_depot).strip() == "": date_depot = None

            # Nettoyer frais
            frais = r[9]
            try: frais = float(frais) if frais else 0
            except: frais = 0

            # INSERT dans archive
            ok_insert = db.query(
                "INSERT INTO archive (avocat_id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
                "sujet,adversaire,remarque,frais_affaire,type_affaire,numero_enquete,"
                "date_depot_dossier,decision_finale,date,cause_romprement) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (aid,r[2],r[3],r[4],r[5],r[6],r[7],r[8],frais,r[10],r[11],
                 date_depot,r[13],r[14],r[15]))

            if not ok_insert:
                messagebox.showerror("Erreur","L'archivage a échoué. L'affaire n'a pas été supprimée.")
                return

            # Seulement si INSERT réussi → supprimer de affaire
            db.query("DELETE FROM affaire WHERE id=%s AND avocat_id=%s",(cid,aid))
            if fen: fen.destroy()
            messagebox.showinfo("Archivée","Affaire archivée avec succès !")
            self.charger()

        except Exception as e:
            messagebox.showerror("Erreur archivage", str(e))

    def exporter_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if not path: return
        doc = SimpleDocTemplate(path, pagesize=landscape(letter))
        styles = getSampleStyleSheet()
        hdrs = [T_("id"),T_("autorite_col"),T_("salle"),T_("type_client_col"),T_("nom_client_col"),T_("adversaire_col"),T_("type_affaire_col"),T_("date_depot_col"),T_("decision_col"),T_("date_report_col"),T_("cause_col")]
        data = [hdrs] + [list(self.tree.item(r,"values")) for r in self.tree.get_children()]
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
        doc.build([Paragraph("Liste des Affaires",styles["Title"]),Spacer(1,12),tbl])
        messagebox.showinfo("Succès","PDF exporté !")

    def afficher_details(self, event=None):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0],"values")
        id_affaire = vals[0]
        aid = db.SESSION.get("avocat_id")

        fen = tk.Toplevel(root); fen.title(f"Affaire — {vals[4]}")
        fen.geometry("750x620"); fen.configure(bg=T.BG); fen.grab_set()

        tk.Frame(fen,bg=T.CYAN,pady=10).pack(fill="x")
        fen.winfo_children()[-1]  # header frame
        hf = fen.winfo_children()[0]
        tk.Label(hf,text=f"⚖  Détails — ID {id_affaire}",bg=T.CYAN,fg=T.BG,
                 font=("Segoe UI",13,"bold")).pack()

        canvas = tk.Canvas(fen,bg=T.BG,highlightthickness=0)
        scrollbar = ttk.Scrollbar(fen,orient="vertical",command=canvas.yview)
        fi = tk.Frame(canvas,bg=T.BG)
        fi.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0),window=fi,anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left",fill="both",expand=True,padx=10,pady=10)
        scrollbar.pack(side="right",fill="y")

        labels = [
            ("Autorité judiciaire","autorite_judiciaire",vals[1]),
            ("Salle / Département","salle_ou_departement",vals[2]),
            ("Type client","type_client",vals[3]),
            ("Nom client","nom_client",vals[4]),
            ("Adversaire","adversaire",vals[5]),
            ("Type affaire","type_affaire",vals[6]),
            ("Date dépôt","date_depot_dossier",vals[7]),
            ("Décision finale","decision_finale",vals[8]),
            ("Date report","date",vals[9]),
            ("Cause romprement","cause_romprement",vals[10]),
        ]
        entries = {}
        for i,(label,col,val) in enumerate(labels):
            tk.Label(fi,text=label+" :",bg=T.BG,fg=T.TEXT2,font=("Segoe UI",10,"bold"),
                     anchor="w").grid(row=i,column=0,sticky="w",padx=18,pady=6)
            e = tk.Entry(fi,font=("Segoe UI",10),bg=T.BG2,fg=T.TEXT,insertbackground=T.CYAN,
                         relief="flat",bd=0,highlightthickness=1,
                         highlightbackground=T.BORDER,highlightcolor=T.CYAN,width=42)
            e.insert(0,val if val else "")
            e.grid(row=i,column=1,padx=14,pady=6,ipady=5,sticky="w")
            entries[col] = e

        bf = tk.Frame(fen,bg=T.BG2,pady=12); bf.pack(fill="x",side="bottom")

        def valider_modif():
            n = {col:e.get().strip() for col,e in entries.items()}
            db.query(
                "UPDATE affaire SET autorite_judiciaire=%s,salle_ou_departement=%s,"
                "type_client=%s,nom_client=%s,adversaire=%s,type_affaire=%s,"
                "date_depot_dossier=%s,decision_finale=%s,date=%s,cause_romprement=%s "
                "WHERE id=%s AND avocat_id=%s",
                (n["autorite_judiciaire"],n["salle_ou_departement"],n["type_client"],
                 n["nom_client"],n["adversaire"],n["type_affaire"],n["date_depot_dossier"],
                 n["decision_finale"],n["date"],n["cause_romprement"],id_affaire,aid))
            messagebox.showinfo("Succès","Affaire modifiée !"); fen.destroy(); self.charger()

        def remporter():
            aujourd_hui = dt_date.today().strftime("%Y-%m-%d")
            if messagebox.askyesno("Remporter",f"Confirmer REMPORTÉE le {aujourd_hui} ?"):
                db.query("UPDATE affaire SET decision_finale=%s,date=%s WHERE id=%s AND avocat_id=%s",
                         ("Gagnée",aujourd_hui,id_affaire,aid))
                entries["decision_finale"].delete(0,tk.END); entries["decision_finale"].insert(0,"Gagnée")
                entries["date"].delete(0,tk.END); entries["date"].insert(0,aujourd_hui)
                messagebox.showinfo("🏆","Affaire GAGNÉE !"); self.charger()

        def saisir_dec():
            win = tk.Toplevel(fen); win.title("Décision"); win.geometry("420x220")
            win.configure(bg=T.BG); win.grab_set()
            tk.Label(win,text="Décision :",bg=T.BG,fg=T.TEXT2,font=("Segoe UI",10,"bold")).pack(pady=(18,4))
            e_dec = T.entry(win,w=36); e_dec.insert(0,entries["decision_finale"].get()); e_dec.pack(ipady=6,pady=4)
            tk.Label(win,text="Date :",bg=T.BG,fg=T.TEXT2,font=("Segoe UI",10,"bold")).pack(pady=(10,4))
            e_dat = T.entry(win,w=36); e_dat.insert(0,entries["date"].get() or dt_date.today().strftime("%Y-%m-%d"))
            e_dat.pack(ipady=6,pady=4)
            def confirmer():
                if not e_dec.get().strip(): messagebox.showwarning("Vide","Saisissez la décision."); return
                db.query("UPDATE affaire SET decision_finale=%s,date=%s WHERE id=%s AND avocat_id=%s",
                         (e_dec.get().strip(),e_dat.get().strip(),id_affaire,aid))
                entries["decision_finale"].delete(0,tk.END); entries["decision_finale"].insert(0,e_dec.get().strip())
                entries["date"].delete(0,tk.END); entries["date"].insert(0,e_dat.get().strip())
                messagebox.showinfo("OK","Décision enregistrée."); win.destroy(); self.charger()
            tk.Button(win,text="✔ Confirmer",command=confirmer,bg=T.CYAN,fg=T.BG,
                      font=("Segoe UI",10,"bold"),relief="flat",padx=18,pady=6,cursor="hand2").pack(pady=14)

        def archiver_detail():
            if messagebox.askyesno("Archiver","Archiver cette affaire ?"):
                self.archiver_par_id(id_affaire, fen)

        for txt,cmd,bg in [
            ("✏️ Modifier",valider_modif,T.CYAN),
            ("🏆 Remporter",remporter,"#27AE60"),
            ("⚖️ Décision",saisir_dec,"#2980B9"),
            ("🗄 Archiver",archiver_detail,"#8E44AD"),
        ]:
            tk.Button(bf,text=txt,command=cmd,bg=bg,fg="white" if bg!=T.CYAN else T.BG,
                      font=("Segoe UI",10,"bold"),relief="flat",padx=14,pady=7,
                      cursor="hand2").pack(side="left",padx=8)
        tk.Button(bf,text="✖ Fermer",command=fen.destroy,bg=T.BG3,fg=T.TEXT2,
                  font=("Segoe UI",10),relief="flat",padx=14,pady=7,
                  cursor="hand2").pack(side="right",padx=12)

# ============================================================
#  PAGE AJOUTER AFFAIRE
# ============================================================
class AjouterAffairePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._parent = parent
        self._titres = {'FR': 'Nouvelle affaire', 'AR': 'قضية جديدة'}
        self._page_active_key = "ajouter_affaire"
        self.frame, self.content = make_page_frame(self, "Nouvelle affaire", "ajouter_affaire")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        c = self.content
        canvas = tk.Canvas(c, bg=T.BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        scroll = ttk.Scrollbar(c, orient="vertical", command=canvas.yview)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)
        fo = tk.Frame(canvas, bg=T.BG)
        canvas.create_window((0,0), window=fo, anchor="nw")
        fo.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def rf(parent, lbl_txt, widget):
            r = tk.Frame(parent, bg=T.BG); r.pack(fill="x", pady=4)
            T.lbl(r, lbl_txt, size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")
            if isinstance(widget, tk.Entry): widget.pack(fill="x", ipady=6, pady=2)
            else: widget.pack(fill="x", pady=2)

        T.section_title(fo, T_("info_generales"), bg=T.BG).pack(fill="x", pady=(0,8))

        # Client combobox
        r_cl = tk.Frame(fo, bg=T.BG); r_cl.pack(fill="x", pady=4)
        T.lbl(r_cl, T_("nom_client"), size=10, bold=True, color=T.TEXT2, bg=T.BG).pack(anchor="w")
        cf = tk.Frame(r_cl, bg=T.BG); cf.pack(fill="x", pady=2)
        self.cb_client = ttk.Combobox(cf, font=("Segoe UI",11), width=46, state="readonly")
        self.cb_client.pack(side="left", fill="x", expand=True, ipady=4)
        tk.Button(cf, text="🔄", bg=T.BG2, fg=T.CYAN, relief="flat",
                  font=("Segoe UI",11), cursor="hand2",
                  command=self._charger_clients).pack(side="left", padx=(6,0))

        self.e_adversaire = T.entry(fo, w=50); rf(fo, T_("adversaire"), self.e_adversaire)
        self.cb_autorite = T.combo(fo, ["Le tribunal","Le conseil","Cour suprême","Conseil d'état","Tribunal administratif","Cour pénale","Tribunal militaire"])
        rf(fo, T_("autorite"), self.cb_autorite)
        self.cb_dept = T.combo(fo, ["Civiles","Immobilières","Commerciales","Familiales","Pénales"])
        rf(fo, T_("departement"), self.cb_dept)
        self.cb_type_client = T.combo(fo, ["Demandeur","Accusé","Défendeur","Victime","Fonctionnaire civil"])
        rf(fo, T_("type_client"), self.cb_type_client)
        self.cb_type_affaire = T.combo(fo, ["Plainte","Convocation directe","Autre"])
        rf(fo, T_("type_affaire"), self.cb_type_affaire)
        self.e_frais = T.entry(fo, w=50); rf(fo, T_("frais"), self.e_frais)
        self.e_enquete = T.entry(fo, w=50); rf(fo, T_("enquete"), self.e_enquete)
        self.e_date = T.entry(fo, w=50); rf(fo, T_("date_depot"), self.e_date)
        self.e_decision = T.entry(fo, w=50); rf(fo, T_("decision"), self.e_decision)
        self.e_report = T.entry(fo, w=50); rf(fo, T_("date_report"), self.e_report)
        self.e_cause = T.entry(fo, w=50); rf(fo, T_("cause"), self.e_cause)

        T.section_title(fo, T_("sujet_remarques"), bg=T.BG).pack(fill="x", pady=(12,6))
        r2 = tk.Frame(fo, bg=T.BG); r2.pack(fill="x", pady=4)
        lf2 = tk.Frame(r2, bg=T.BG); lf2.pack(side="left", fill="x", expand=True, padx=(0,12))
        T.lbl(lf2,T_("sujet"),size=10,bold=True,color=T.TEXT2,bg=T.BG).pack(anchor="w")
        self.t_sujet = tk.Text(lf2,height=4,bg=T.BG3,fg=T.TEXT,font=T.FONT_BODY,
                               relief="flat",insertbackground=T.TEXT,
                               highlightbackground=T.BORDER,highlightthickness=1)
        self.t_sujet.pack(fill="x")
        rf2 = tk.Frame(r2, bg=T.BG); rf2.pack(side="left", fill="x", expand=True)
        T.lbl(rf2,T_("remarque"),size=10,bold=True,color=T.TEXT2,bg=T.BG).pack(anchor="w")
        self.t_remarque = tk.Text(rf2,height=4,bg=T.BG3,fg=T.TEXT,font=T.FONT_BODY,
                                  relief="flat",insertbackground=T.TEXT,
                                  highlightbackground=T.BORDER,highlightthickness=1)
        self.t_remarque.pack(fill="x")

        br = tk.Frame(fo, bg=T.BG); br.pack(fill="x", pady=20)
        T.btn(br,T_("enregistrer"),cmd=self.ajouter,w=30,color=T.SUCCESS,hover="#1E8449").pack(side="left",padx=4,ipady=5)
        T.btn(br,T_("annuler"),cmd=self.reset,w=16,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4,ipady=5)

    def on_show(self): self._charger_clients()

    def _charger_clients(self):
        aid = db.SESSION.get("avocat_id")
        rows = db.query("SELECT nom,prenom FROM client WHERE avocat_id=%s ORDER BY nom",(aid,),fetch=True)
        self.cb_client["values"] = [f"{r[0]} {r[1]}" for r in rows] if rows else []

    def reset(self):
        self.cb_client.set(""); self.e_adversaire.delete(0,"end")
        self.cb_autorite.set(""); self.cb_dept.set("")
        self.cb_type_client.set(""); self.cb_type_affaire.set("")
        self.e_frais.delete(0,"end"); self.e_enquete.delete(0,"end")
        self.e_date.delete(0,"end"); self.e_decision.delete(0,"end")
        self.e_report.delete(0,"end"); self.e_cause.delete(0,"end")
        self.t_sujet.delete("1.0","end"); self.t_remarque.delete("1.0","end")

    def ajouter(self):
        aid = db.SESSION.get("avocat_id")
        nom_client = self.cb_client.get().strip()
        adversaire = self.e_adversaire.get().strip()
        if not nom_client or not adversaire:
            messagebox.showwarning("Requis","Nom client et adversaire obligatoires."); return
        # Valider frais
        frais_str = self.e_frais.get().strip().replace(",", ".") or "0"
        try:
            frais = float(frais_str)
            if frais > 99999999.99:
                messagebox.showwarning("Frais invalide", "Le montant des frais est trop élevé."); return
        except ValueError:
            messagebox.showwarning("Frais invalide", "Les frais doivent être un nombre (ex: 5000)."); return

        # Valider date depot
        date_depot = self.e_date.get().strip() or None
        if date_depot and len(date_depot) != 10:
            messagebox.showwarning("Date invalide", "Format date: AAAA-MM-JJ (ex: 2024-01-15)"); return

        db.query(
            "INSERT INTO affaire (avocat_id,adversaire,autorite_judiciaire,salle_ou_departement,"
            "type_client,nom_client,frais_affaire,type_affaire,sujet,remarque,"
            "numero_enquete,date_depot_dossier,decision_finale,date,cause_romprement) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (aid, adversaire, self.cb_autorite.get(), self.cb_dept.get(),
             self.cb_type_client.get(), nom_client, frais,
             self.cb_type_affaire.get(), self.t_sujet.get("1.0","end").strip(),
             self.t_remarque.get("1.0","end").strip(), self.e_enquete.get().strip(),
             date_depot, self.e_decision.get().strip(),
             self.e_report.get().strip(), self.e_cause.get().strip()))
        messagebox.showinfo("Succès","Affaire ajoutée !"); self.reset()

# ============================================================
#  PAGE CLIENTS
# ============================================================
class ClientsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._parent = parent
        self._titres = {'FR': 'Gestion Clients', 'AR': 'إدارة الموكلين'}
        self._page_active_key = "clients"
        self.frame, self.content = make_page_frame(self, "Gestion Clients", "clients")
        self.frame.pack(fill="both", expand=True)
        self._photo_ref = None
        self._build()

    def _build(self):
        c = self.content

        # ── Formulaire ──
        form_card = T.card(c, padx=20, pady=16); form_card.pack(fill="x", pady=(0,12))
        T.section_title(form_card, T_("info_client"), bg=T.BG2).pack(fill="x", pady=(0,10))

        # Zone principale = champs + photo côte à côte
        main_row = tk.Frame(form_card, bg=T.BG2); main_row.pack(fill="x", pady=4)

        # Colonne gauche — champs
        left_col = tk.Frame(main_row, bg=T.BG2); left_col.pack(side="left", fill="x", expand=True)

        e_id_f = tk.Frame(left_col, bg=T.BG2); e_id_f.pack(fill="x", pady=(0,4))
        T.lbl(e_id_f, "ID", size=9, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
        self.e_id = T.entry(e_id_f, w=20); self.e_id.pack(anchor="w", ipady=5, pady=2)

        def fr(parent, items):
            r = tk.Frame(parent, bg=T.BG2); r.pack(fill="x", pady=3)
            entries = []
            for label, show in items:
                f = tk.Frame(r, bg=T.BG2); f.pack(side="left", fill="x", expand=True, padx=4)
                T.lbl(f, label, size=9, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w")
                e = T.entry(f, w=22, show=show); e.pack(fill="x", ipady=5, pady=2)
                entries.append(e)
            return entries

        (self.e_nom, self.e_prenom), = [fr(left_col, [(T_("nom_col"), ""), (T_("prenom"), "")])]
        (self.e_adresse, self.e_email), = [fr(left_col, [(T_("adresse"), ""), ("Email", "")])]
        (self.e_tel,), = [fr(left_col, [(T_("telephone"), "")])]

        # Colonne droite — photo
        right_col = tk.Frame(main_row, bg=T.BG2, padx=14); right_col.pack(side="left", anchor="n", pady=4)
        T.lbl(right_col, "📷 Photo client", size=9, bold=True, color=T.TEXT2, bg=T.BG2).pack(anchor="w", pady=(0,6))

        self.lbl_photo = tk.Label(right_col, bg=T.BG3, width=10, height=5,
                                   text="👤", font=("Segoe UI", 28),
                                   fg=T.TEXT2, cursor="hand2",
                                   relief="flat",
                                   highlightbackground=T.BORDER, highlightthickness=1)
        self.lbl_photo.pack(pady=(0,6))
        self.lbl_photo.bind("<Button-1>", lambda e: self.changer_photo())

        tk.Button(right_col, text="📷 Choisir photo",
                  bg=T.BG3, fg=T.CYAN, font=("Segoe UI", 8),
                  relief="flat", cursor="hand2",
                  command=self.changer_photo).pack(fill="x")
        tk.Button(right_col, text="✖ Supprimer photo",
                  bg=T.BG3, fg=T.ACCENT2, font=("Segoe UI", 8),
                  relief="flat", cursor="hand2",
                  command=self.supprimer_photo).pack(fill="x", pady=(3,0))

        # Boutons action
        br = tk.Frame(form_card, bg=T.BG2); br.pack(fill="x", pady=(10,0))
        T.btn(br, T_("ajouter"),   cmd=self.ajouter,   w=14, color=T.SUCCESS, hover="#1E8449").pack(side="left", padx=4, ipady=4)
        T.btn(br, T_("modifier"),  cmd=self.modifier,  w=14).pack(side="left", padx=4, ipady=4)
        T.btn(br, T_("supprimer"), cmd=self.supprimer, w=14, color=T.BG3, hover=T.BORDER, fg=T.ACCENT2).pack(side="left", padx=4, ipady=4)
        T.btn(br, T_("joindre"),   cmd=self.joindre,   w=14, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4, ipady=4)
        T.btn(br, "📄 Fiche PDF",  cmd=self.fiche_pdf,       w=14, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="left", padx=4, ipady=4)
        T.btn(br, "⬇ Télécharger", cmd=self.telecharger_fichier, w=14, color=T.BG3, hover=T.BORDER, fg=T.CYAN).pack(side="left", padx=4, ipady=4)

        # Tableau
        T.style_treeview(None)
        self.tree = ttk.Treeview(c, columns=(1,2,3,4,5,6,7), show="headings", style="M.Treeview", height=10)
        for i,(h,w) in enumerate(zip([T_("id"),T_("nom_col"),T_("prenom"),T_("adresse"),T_("email"),T_("telephone"),T_("document")],
                                     [40,120,120,160,160,110,130]),1):
            self.tree.heading(i, text=h); self.tree.column(i, width=w, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.afficher_fiche)
        sb = ttk.Scrollbar(c, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

    def on_show(self): self.charger()

    def charger(self):
        aid = db.SESSION.get("avocat_id")
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query("SELECT id,nom,prenom,adresse,email,telephone,fichier_nom FROM client WHERE avocat_id=%s", (aid,), fetch=True)
        for r in rows: self.tree.insert("", "end", values=r)

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        for e, val in zip([self.e_id, self.e_nom, self.e_prenom, self.e_adresse, self.e_email, self.e_tel], v):
            e.config(state="normal"); e.delete(0, "end"); e.insert(0, val)
        # Charger la photo du client sélectionné
        cid = v[0]
        rows = db.query("SELECT photo_client FROM client WHERE id=%s", (cid,), fetch=True)
        if rows and rows[0][0]:
            self._afficher_photo(bytes(rows[0][0]))
        else:
            self.lbl_photo.config(image="", text="👤", font=("Segoe UI", 28))
            self._photo_ref = None

    def _afficher_photo(self, data):
        try:
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            img = img.resize((100, 100), Image.LANCZOS)
            self._photo_ref = ImageTk.PhotoImage(img)
            self.lbl_photo.config(image=self._photo_ref, text="", width=100, height=100)
        except: pass

    def changer_photo(self):
        cid = self.e_id.get().strip()
        if not cid: messagebox.showwarning("Sélection", "Sélectionnez d'abord un client."); return
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            with open(path, "rb") as f: data = f.read()
            # Vérifier/ajouter colonne
            try:
                cx = db.get_conn(); cur = cx.cursor()
                cur.execute("SHOW COLUMNS FROM client LIKE 'photo_client'")
                if not cur.fetchone():
                    cur.execute("ALTER TABLE client ADD COLUMN photo_client LONGBLOB")
                cx.commit(); cx.close()
            except: pass
            db.query("UPDATE client SET photo_client=%s WHERE id=%s AND avocat_id=%s",
                     (data, cid, db.SESSION.get("avocat_id")))
            self._afficher_photo(data)
            messagebox.showinfo("Succès", "Photo ajoutée !")

    def supprimer_photo(self):
        cid = self.e_id.get().strip()
        if not cid: messagebox.showwarning("Sélection", "Sélectionnez d'abord un client."); return
        db.query("UPDATE client SET photo_client=NULL WHERE id=%s AND avocat_id=%s",
                 (cid, db.SESSION.get("avocat_id")))
        self.lbl_photo.config(image="", text="👤", font=("Segoe UI", 28), width=10, height=5)
        self._photo_ref = None
        messagebox.showinfo("OK", "Photo supprimée.")

    def ajouter(self):
        aid = db.SESSION.get("avocat_id")
        vals = [self.e_nom.get().strip(), self.e_prenom.get().strip(),
                self.e_adresse.get().strip(), self.e_email.get().strip(), self.e_tel.get().strip()]
        if not all(vals): messagebox.showwarning("Vide", "Remplissez tous les champs."); return
        db.query("INSERT INTO client (avocat_id,nom,prenom,adresse,email,telephone) VALUES (%s,%s,%s,%s,%s,%s)",
                 (aid, *vals))
        messagebox.showinfo("Succès", "Client ajouté !"); self.charger()

    def modifier(self):
        cid = self.e_id.get().strip()
        if not cid: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
        aid = db.SESSION.get("avocat_id")
        db.query("UPDATE client SET nom=%s,prenom=%s,adresse=%s,email=%s,telephone=%s WHERE id=%s AND avocat_id=%s",
                 (self.e_nom.get(), self.e_prenom.get(), self.e_adresse.get(),
                  self.e_email.get(), self.e_tel.get(), cid, aid))
        messagebox.showinfo("Succès", "Client modifié !"); self.charger()

    def supprimer(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
        if messagebox.askyesno("Confirmation", "Supprimer ce client ?"):
            cid = self.tree.item(sel[0], "values")[0]
            db.query("DELETE FROM client WHERE id=%s AND avocat_id=%s", (cid, db.SESSION.get("avocat_id")))
            self.charger()

    def joindre(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
        cid = self.tree.item(sel[0], "values")[0]
        path = filedialog.askopenfilename()
        if path:
            with open(path, "rb") as f: contenu = f.read()
            db.query("UPDATE client SET fichier_nom=%s,fichier_contenu=%s WHERE id=%s AND avocat_id=%s",
                     (os.path.basename(path), contenu, cid, db.SESSION.get("avocat_id")))
            messagebox.showinfo("Succès", "Fichier joint !"); self.charger()

    def telecharger_fichier(self):
        """Télécharge le fichier joint du client sélectionné."""
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
        cid = self.tree.item(sel[0], "values")[0]
        rows = db.query("SELECT fichier_nom, fichier_contenu FROM client WHERE id=%s", (cid,), fetch=True)
        if not rows or not rows[0][0] or not rows[0][1]:
            messagebox.showwarning("Aucun fichier", "Ce client n'a pas de fichier joint."); return
        nom_fichier = rows[0][0]
        contenu = bytes(rows[0][1])
        # Demander où sauvegarder
        path = filedialog.asksaveasfilename(
            initialfile=nom_fichier,
            defaultextension=os.path.splitext(nom_fichier)[1],
            filetypes=[("Tous les fichiers", "*.*"), ("PDF", "*.pdf")])
        if path:
            with open(path, "wb") as f:
                f.write(contenu)
            messagebox.showinfo("Téléchargé", "Fichier sauvegardé :\n" + str(path))
            # Ouvrir automatiquement
            try: os.startfile(path)
            except: pass

    def fiche_pdf(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
        self._generer_fiche_pdf()

    def afficher_fiche(self, event=None):
        """Double-clic : fenêtre avec infos + PDF joint + bouton fiche PDF."""
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0], "values")
        cid = v[0]

        # Récupérer toutes les données du client
        rows = db.query(
            "SELECT id,nom,prenom,adresse,email,telephone,fichier_nom,fichier_contenu,photo_client "
            "FROM client WHERE id=%s", (cid,), fetch=True)
        if not rows: return
        r = rows[0]

        win = tk.Toplevel(root)
        win.title(f"Client — {r[1]} {r[2]}")
        win.geometry("660x640")
        win.configure(bg=T.BG)
        win.grab_set()

        # Header
        hdr = tk.Frame(win, bg=T.CYAN, pady=10); hdr.pack(fill="x")
        tk.Label(hdr, text=f"👤  {r[1]} {r[2]}", bg=T.CYAN, fg=T.BG,
                 font=("Segoe UI", 13, "bold")).pack()

        body = tk.Frame(win, bg=T.BG); body.pack(fill="both", expand=True, padx=20, pady=16)

        # Photo + infos côte à côte
        top = tk.Frame(body, bg=T.BG); top.pack(fill="x", pady=(0,14))

        # Photo
        photo_frame = tk.Frame(top, bg=T.BG2, padx=8, pady=8,
                                highlightbackground=T.BORDER, highlightthickness=1)
        photo_frame.pack(side="left", padx=(0,16))
        lbl_p = tk.Label(photo_frame, text="👤", bg=T.BG2, fg=T.TEXT2,
                          font=("Segoe UI", 30), width=7, height=4)
        lbl_p.pack()
        if r[8]:
            try:
                img = Image.open(io.BytesIO(bytes(r[8]))).convert("RGBA")
                img = img.resize((90, 90), Image.LANCZOS)
                _ref = ImageTk.PhotoImage(img)
                lbl_p.config(image=_ref, text="", width=90, height=90)
                lbl_p.image = _ref
            except: pass

        # Infos
        info_frame = tk.Frame(top, bg=T.BG); info_frame.pack(side="left", fill="x", expand=True)
        infos = [
            ("📛 Nom complet", f"{r[1]} {r[2]}"),
            ("🏠 Adresse",     r[3] or "-"),
            ("📧 Email",       r[4] or "-"),
            ("📞 Téléphone",   r[5] or "-"),
        ]
        for label, val in infos:
            row = tk.Frame(info_frame, bg=T.BG); row.pack(fill="x", pady=3)
            tk.Label(row, text=label + " :", bg=T.BG, fg=T.TEXT2,
                     font=("Segoe UI", 10, "bold"), width=16, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg=T.BG, fg=T.TEXT,
                     font=("Segoe UI", 10)).pack(side="left", padx=6)

        # Séparateur
        tk.Frame(body, bg=T.BORDER, height=1).pack(fill="x", pady=(0,12))

        # Zone PDF joint
        pdf_frame = tk.Frame(body, bg=T.BG); pdf_frame.pack(fill="x")
        nom_fichier = r[6] or None
        contenu_fichier = r[7] or None

        if nom_fichier and contenu_fichier:
            tk.Label(pdf_frame, text=f"📎 Fichier joint : {nom_fichier}",
                     bg=T.BG, fg=T.CYAN, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0,6))

            def voir_pdf():
                # Sauvegarder temporairement et ouvrir
                import tempfile, subprocess as sp
                ext = os.path.splitext(nom_fichier)[1].lower()
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
                tmp.write(bytes(contenu_fichier))
                tmp.close()
                try:
                    os.startfile(tmp.name)  # Windows
                except:
                    sp.Popen(["xdg-open", tmp.name])  # Linux

            T.btn(pdf_frame, f"👁 Ouvrir {nom_fichier}", cmd=voir_pdf,
                  w=36, color=T.BG2, hover=T.BORDER, fg=T.CYAN).pack(anchor="w")
        else:
            tk.Label(pdf_frame, text="📎 Aucun fichier joint",
                     bg=T.BG, fg=T.TEXT2, font=("Segoe UI", 10, "italic")).pack(anchor="w")

        # ── Affaires associées ──
        tk.Frame(body, bg=T.BORDER, height=1).pack(fill="x", pady=(8,8))
        tk.Label(body, text="⚖ Affaires associées", bg=T.BG, fg=T.CYAN,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,6))

        affaires = db.query(
            "SELECT type_affaire,adversaire,date_depot_dossier,decision_finale FROM affaire "
            "WHERE nom_client LIKE %s AND avocat_id=%s",
            (f"%{r[1]}%", db.SESSION.get("avocat_id")), fetch=True)

        if affaires:
            aff_frame = tk.Frame(body, bg=T.BG2,
                                  highlightbackground=T.BORDER, highlightthickness=1)
            aff_frame.pack(fill="x")
            hdrs = ["Type affaire", "Adversaire", "Date dépôt", "Décision"]
            wds  = [120, 140, 100, 140]
            hdr_row = tk.Frame(aff_frame, bg=T.BG3); hdr_row.pack(fill="x")
            for h, w in zip(hdrs, wds):
                tk.Label(hdr_row, text=h, bg=T.BG3, fg=T.CYAN,
                         font=("Segoe UI", 9, "bold"), width=w//7, anchor="w").pack(side="left", padx=4)
            for i, a in enumerate(affaires):
                row_bg = T.BG2 if i % 2 == 0 else T.BG3
                aff_row = tk.Frame(aff_frame, bg=row_bg); aff_row.pack(fill="x")
                for val, w in zip(a, wds):
                    tk.Label(aff_row, text=str(val or "-"), bg=row_bg, fg=T.TEXT,
                             font=("Segoe UI", 9), width=w//7, anchor="w").pack(side="left", padx=4, pady=2)
        else:
            tk.Label(body, text="Aucune affaire enregistrée pour ce client.",
                     bg=T.BG, fg=T.TEXT2, font=("Segoe UI", 9, "italic")).pack(anchor="w")

        # Boutons bas
        btn_frame = tk.Frame(win, bg=T.BG2, pady=12); btn_frame.pack(fill="x", side="bottom")
        T.btn(btn_frame, "📄 Générer fiche PDF", cmd=lambda: self._generer_fiche_pdf(),
              w=20, color=T.CYAN, hover="#17A589", fg=T.BG).pack(side="left", padx=8)

        # Bouton télécharger fichier joint
        if nom_fichier and contenu_fichier:
            def dl_fichier():
                path = filedialog.asksaveasfilename(
                    initialfile=nom_fichier,
                    defaultextension=os.path.splitext(nom_fichier)[1],
                    filetypes=[("Tous les fichiers","*.*")])
                if path:
                    with open(path,"wb") as f: f.write(bytes(contenu_fichier))
                    messagebox.showinfo("✅ Téléchargé", f"Fichier sauvegardé !")
                    try: os.startfile(path)
                    except: pass
            T.btn(btn_frame, f"⬇ Télécharger fichier", cmd=dl_fichier,
                  w=20, color=T.BG3, hover=T.BORDER, fg=T.CYAN).pack(side="left", padx=8)

        T.btn(btn_frame, "✖ Fermer", cmd=win.destroy,
              w=14, color=T.BG3, hover=T.BORDER, fg=T.TEXT2).pack(side="right", padx=12)

    def _generer_fiche_pdf(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection", "Sélectionnez un client."); return
        v = self.tree.item(sel[0], "values")
        cid = v[0]

        # Récupérer données complètes + affaires du client
        rows = db.query("SELECT id,nom,prenom,adresse,email,telephone,photo_client FROM client WHERE id=%s", (cid,), fetch=True)
        if not rows: return
        r = rows[0]
        nom_complet = f"{r[1]} {r[2]}"

        affaires = db.query(
            "SELECT type_affaire,adversaire,date_depot_dossier,decision_finale FROM affaire "
            "WHERE nom_client LIKE %s AND avocat_id=%s",
            (f"%{r[1]}%", db.SESSION.get("avocat_id")), fetch=True)

        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"Fiche_{nom_complet.replace(' ','_')}.pdf",
            filetypes=[("PDF", "*.pdf")])
        if not path: return

        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors as rl_colors

        doc = SimpleDocTemplate(path, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # En-tête
        title_style = ParagraphStyle("title", fontSize=18, fontName="Helvetica-Bold",
                                      textColor=rl_colors.HexColor("#1ABC9C"), spaceAfter=6)
        sub_style = ParagraphStyle("sub", fontSize=11, textColor=rl_colors.HexColor("#555555"), spaceAfter=20)

        story.append(Paragraph("⚖ CaseCraft — Fiche Client", title_style))
        story.append(Paragraph(f"Généré le {dt_date.today().strftime('%d/%m/%Y')}", sub_style))

        # Photo + infos côte à côte
        photo_cell = ""
        if r[6]:
            try:
                img_data = io.BytesIO(bytes(r[6]))
                pil_img = Image.open(img_data).convert("RGB")
                pil_img = pil_img.resize((100, 100))
                img_buf = io.BytesIO()
                pil_img.save(img_buf, format="JPEG")
                img_buf.seek(0)
                photo_cell = RLImage(img_buf, width=3*cm, height=3*cm)
            except: photo_cell = Paragraph("(pas de photo)", styles["Normal"])
        else:
            photo_cell = Paragraph("(pas de photo)", styles["Normal"])

        info_style = ParagraphStyle("info", fontSize=10, leading=16)
        infos = Paragraph(
            f"<b>Nom :</b> {r[1]} {r[2]}<br/>"
            f"<b>Adresse :</b> {r[3] or '-'}<br/>"
            f"<b>Email :</b> {r[4] or '-'}<br/>"
            f"<b>Téléphone :</b> {r[5] or '-'}",
            info_style)

        info_table = Table([[photo_cell, infos]], colWidths=[3.5*cm, 13*cm])
        info_table.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("BACKGROUND", (0,0), (-1,-1), rl_colors.HexColor("#F7F7F7")),
            ("BOX", (0,0), (-1,-1), 0.5, rl_colors.HexColor("#CCCCCC")),
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [rl_colors.HexColor("#F7F7F7")]),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*cm))

        # Affaires du client
        story.append(Paragraph("Affaires associées", ParagraphStyle("h2", fontSize=13,
            fontName="Helvetica-Bold", textColor=rl_colors.HexColor("#1ABC9C"), spaceAfter=8)))

        if affaires:
            aff_data = [["Type affaire", "Adversaire", "Date dépôt", "Décision"]]
            for a in affaires:
                aff_data.append([str(a[0] or "-"), str(a[1] or "-"),
                                  str(a[2] or "-"), str(a[3] or "-")])
            aff_table = Table(aff_data, colWidths=[4*cm, 4*cm, 3.5*cm, 5*cm])
            aff_table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), rl_colors.HexColor("#0D1B2A")),
                ("TEXTCOLOR", (0,0), (-1,0), rl_colors.HexColor("#1ABC9C")),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ("BACKGROUND", (0,1), (-1,-1), rl_colors.HexColor("#F0F0F0")),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [rl_colors.white, rl_colors.HexColor("#F0F0F0")]),
                ("GRID", (0,0), (-1,-1), 0.5, rl_colors.HexColor("#CCCCCC")),
                ("FONTSIZE", (0,0), (-1,-1), 9),
            ]))
            story.append(aff_table)
        else:
            story.append(Paragraph("Aucune affaire enregistrée pour ce client.", styles["Normal"]))

        doc.build(story)
        messagebox.showinfo("PDF créé", "Fiche enregistrée :\n" + str(path))

# ============================================================
#  PAGE FINANCES
# ============================================================
class FinancesPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._parent = parent
        self._titres = {'FR': 'Gestion Financière', 'AR': 'الإدارة المالية'}
        self._page_active_key = "finances"
        self.frame, self.content = make_page_frame(self, "Gestion Financière", "finances")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        c = self.content
        form_card = T.card(c, padx=20, pady=16); form_card.pack(fill="x", pady=(0,12))
        T.section_title(form_card,T_("nouveau_paiement"),bg=T.BG2).pack(fill="x",pady=(0,10))

        r_lbl = tk.Frame(form_card, bg=T.BG2); r_lbl.pack(fill="x", pady=(0,2))
        for lbl_txt in ["ID",T_("nom_client2"),T_("montant_payer"),T_("montant_paye"),T_("date_paiement")]:
            col = tk.Frame(r_lbl, bg=T.BG2); col.pack(side="left", fill="x", expand=True, padx=6)
            T.lbl(col,lbl_txt,size=9,bold=True,color=T.TEXT2,bg=T.BG2).pack(anchor="w")

        r = tk.Frame(form_card, bg=T.BG2); r.pack(fill="x", pady=4)
        self.e_id = T.entry(r,w=8); self.e_id.pack(side="left",fill="x",expand=True,padx=6,ipady=6)
        self.cb_nom = ttk.Combobox(r,font=("Segoe UI",11),width=18,state="normal")
        self.cb_nom.pack(side="left",fill="x",expand=True,padx=6,ipady=4)
        tk.Button(r,text="🔄",bg=T.BG2,fg=T.CYAN,relief="flat",font=("Segoe UI",11),cursor="hand2",
                  command=self._charger_clients).pack(side="left",padx=(0,6))
        self.e_montant = T.entry(r,w=12); self.e_montant.pack(side="left",fill="x",expand=True,padx=6,ipady=6)
        self.e_montant.bind("<KeyRelease>", self.calculer)
        self.e_paye = T.entry(r,w=12); self.e_paye.pack(side="left",fill="x",expand=True,padx=6,ipady=6)
        self.e_paye.bind("<KeyRelease>", self.calculer)
        self.e_date = T.entry(r,w=14); self.e_date.pack(side="left",fill="x",expand=True,padx=6,ipady=6)

        r2 = tk.Frame(form_card, bg=T.BG2); r2.pack(fill="x", pady=4)
        T.lbl(r2,T_("montant_auto"),size=9,bold=True,color=T.CYAN,bg=T.BG2).pack(anchor="w")
        self.e_restant = T.entry(r2,w=20); self.e_restant.pack(anchor="w",ipady=6,pady=2)
        self.e_restant.config(state="readonly")

        br = tk.Frame(form_card, bg=T.BG2); br.pack(fill="x", pady=(10,0))
        T.btn(br,T_("enregistrer2"),cmd=self.ajouter,w=16,color=T.SUCCESS,hover="#1E8449").pack(side="left",padx=4,ipady=4)
        T.btn(br,T_("modifier"),cmd=self.modifier,w=14).pack(side="left",padx=4,ipady=4)
        T.btn(br,T_("supprimer"),cmd=self.supprimer,w=14,color=T.BG3,hover=T.BORDER,fg=T.ACCENT2).pack(side="left",padx=4,ipady=4)
        T.btn(br,T_("export_pdf"),cmd=self.exporter_pdf,w=12,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4,ipady=4)

        T.style_treeview(None)
        self.tree = ttk.Treeview(c,columns=(1,2,3,4,5,6),show="headings",style="M.Treeview",height=14)
        for i,(h,w) in enumerate(zip([T_("id"),T_("nom_col"),T_("montant_col"),T_("paye_col"),T_("restant_col"),T_("date_col")],[50,160,110,110,110,120]),1):
            self.tree.heading(i,text=h); self.tree.column(i,width=w,anchor="center")
        self.tree.bind("<<TreeviewSelect>>",self.on_select)
        sb = ttk.Scrollbar(c,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left",fill="both",expand=True)
        sb.pack(side="left",fill="y")

    def on_show(self): self._charger_clients(); self.charger()

    def _charger_clients(self):
        aid = db.SESSION.get("avocat_id")
        rows = db.query("SELECT nom,prenom FROM client WHERE avocat_id=%s ORDER BY nom",(aid,),fetch=True)
        self.cb_nom["values"] = [f"{r[0]} {r[1]}" for r in rows] if rows else []

    def calculer(self, event=None):
        try:
            self.e_restant.config(state="normal")
            self.e_restant.delete(0,"end")
            self.e_restant.insert(0,str(round(float(self.e_montant.get() or 0)-float(self.e_paye.get() or 0),2)))
            self.e_restant.config(state="readonly")
        except: pass

    def charger(self):
        aid = db.SESSION.get("avocat_id")
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query("SELECT id,Nom_client,montant,montant_payee,montant_restant,date_paiement FROM financement WHERE avocat_id=%s",(aid,),fetch=True)
        for r in rows: self.tree.insert("","end",values=r)

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0],"values")
        self.e_id.delete(0,"end"); self.e_id.insert(0,v[0])
        self.cb_nom.set(v[1])
        self.e_montant.delete(0,"end"); self.e_montant.insert(0,v[2])
        self.e_paye.delete(0,"end"); self.e_paye.insert(0,v[3])
        self.e_restant.config(state="normal"); self.e_restant.delete(0,"end"); self.e_restant.insert(0,v[4]); self.e_restant.config(state="readonly")
        self.e_date.delete(0,"end"); self.e_date.insert(0,v[5])

    def ajouter(self):
        aid = db.SESSION.get("avocat_id")
        nom = self.cb_nom.get().strip()
        if not all([nom,self.e_montant.get(),self.e_paye.get(),self.e_date.get()]):
            messagebox.showwarning("Vide","Remplissez tous les champs."); return
        db.query("INSERT INTO financement (avocat_id,Nom_client,montant,montant_payee,montant_restant,date_paiement) VALUES (%s,%s,%s,%s,%s,%s)",
                 (aid,nom,self.e_montant.get(),self.e_paye.get(),self.e_restant.get(),self.e_date.get()))
        messagebox.showinfo("Succès","Paiement enregistré !"); self.charger()

    def modifier(self):
        cid = self.e_id.get().strip()
        if not cid: messagebox.showwarning("Sélection","Sélectionnez un paiement."); return
        db.query("UPDATE financement SET Nom_client=%s,montant=%s,montant_payee=%s,montant_restant=%s,date_paiement=%s WHERE id=%s AND avocat_id=%s",
                 (self.cb_nom.get(),self.e_montant.get(),self.e_paye.get(),self.e_restant.get(),self.e_date.get(),cid,db.SESSION.get("avocat_id")))
        messagebox.showinfo("Succès","Modifié !"); self.charger()

    def supprimer(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection","Sélectionnez une ligne."); return
        if messagebox.askyesno("Confirmation","Supprimer ?"):
            cid = self.tree.item(sel[0],"values")[0]
            db.query("DELETE FROM financement WHERE id=%s AND avocat_id=%s",(cid,db.SESSION.get("avocat_id")))
            self.charger()

    def exporter_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if not path: return
        doc = SimpleDocTemplate(path,pagesize=letter)
        styles = getSampleStyleSheet()
        data = [["ID","Nom","Montant","Payé","Restant","Date"]] + [list(self.tree.item(r,"values")) for r in self.tree.get_children()]
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
        doc.build([Paragraph("Rapport Financier",styles["Title"]),Spacer(1,12),tbl])
        messagebox.showinfo("Succès","PDF exporté !")

# ============================================================
#  PAGE CALENDRIER
# ============================================================
class CalendrierPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._parent = parent
        self._titres = {'FR': 'Calendrier des audiences', 'AR': 'جدول الجلسات'}
        self._page_active_key = "calendrier"
        self.frame, self.content = make_page_frame(self, "Calendrier des audiences", "calendrier")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        c = self.content
        toolbar = T.card(c,padx=12,pady=10); toolbar.pack(fill="x",pady=(0,12))
        tk.Label(toolbar,text="🔍",bg=T.BG2,fg=T.CYAN,font=("Segoe UI",13)).pack(side="left",padx=(0,8))
        self.e_search = T.entry(toolbar,w=50)
        self.e_search.pack(side="left",fill="x",expand=True,ipady=6)
        self.e_search.bind("<Return>",lambda e:self.rechercher())
        T.btn(toolbar,T_("rechercher"),cmd=self.rechercher,w=14).pack(side="left",padx=6)
        T.btn(toolbar,T_("actualiser"),cmd=self.charger,w=12,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4)
        T.btn(toolbar,T_("pdf"),cmd=self.exporter_pdf,w=14,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4)

        T.style_treeview(None)
        self.tree = ttk.Treeview(c,columns=tuple(range(1,12)),show="headings",style="M.Treeview",height=20)
        for i,(h,w) in enumerate(zip([T_("id"),T_("autorite_col"),T_("salle"),T_("type_client_col"),T_("nom_client_col"),T_("adversaire_col"),T_("type_affaire_col"),T_("date_depot_col"),T_("decision_col"),T_("date_report_col"),T_("cause_col")],
                                     [40,120,90,100,120,120,110,100,110,100,120]),1):
            self.tree.heading(i,text=h); self.tree.column(i,width=w,anchor="center")
        sb = ttk.Scrollbar(c,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left",fill="both",expand=True)
        sb.pack(side="left",fill="y")

    def on_show(self): self.charger()

    def charger(self):
        aid = db.SESSION.get("avocat_id")
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query(
            "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
            "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
            "FROM affaire WHERE avocat_id=%s ORDER BY date_depot_dossier ASC",(aid,),fetch=True)
        for r in rows: self.tree.insert("","end",values=r)

    def rechercher(self):
        aid = db.SESSION.get("avocat_id"); terme = self.e_search.get().strip()
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query(
            "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,"
            "adversaire,type_affaire,date_depot_dossier,decision_finale,date,cause_romprement "
            "FROM affaire WHERE avocat_id=%s AND (nom_client LIKE %s OR adversaire LIKE %s OR type_affaire LIKE %s) "
            "ORDER BY date_depot_dossier ASC",(aid,f"%{terme}%",f"%{terme}%",f"%{terme}%"),fetch=True)
        for r in rows: self.tree.insert("","end",values=r)

    def exporter_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if not path: return
        doc = SimpleDocTemplate(path,pagesize=landscape(letter))
        styles = getSampleStyleSheet()
        hdrs = [T_("id"),T_("autorite_col"),T_("salle"),T_("type_client_col"),T_("nom_client_col"),T_("adversaire_col"),T_("type_affaire_col"),T_("date_depot_col"),T_("decision_col"),T_("date_report_col"),T_("cause_col")]
        data = [hdrs]+[list(self.tree.item(r,"values")) for r in self.tree.get_children()]
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
        doc.build([Paragraph("Calendrier",styles["Title"]),Spacer(1,12),tbl])
        messagebox.showinfo("Succès","PDF exporté !")

# ============================================================
#  PAGE ARCHIVES
# ============================================================
class ArchivesPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=T.BG)
        self._parent = parent
        self._titres = {'FR': 'Archives', 'AR': 'الأرشيف'}
        self._page_active_key = "archives"
        self.frame, self.content = make_page_frame(self, "Archives", "archives")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        c = self.content
        toolbar = T.card(c,padx=12,pady=10); toolbar.pack(fill="x",pady=(0,12))
        T.btn(toolbar,T_("supprimer"),cmd=self.supprimer,w=14,color=T.BG3,hover=T.BORDER,fg=T.ACCENT2).pack(side="left",padx=4)
        T.btn(toolbar,T_("filtrer"),cmd=self.filtrer,w=14,color=T.BG3,hover=T.BORDER,fg=T.CYAN).pack(side="left",padx=4)
        T.btn(toolbar,T_("actualiser"),cmd=self.charger,w=12,color=T.BG3,hover=T.BORDER,fg=T.TEXT2).pack(side="left",padx=4)

        T.style_treeview(None)
        cols = tuple(range(1,16))
        self.tree = ttk.Treeview(c,columns=cols,show="headings",style="M.Treeview",height=20)
        hdrs = [T_("id"),T_("autorite_col"),T_("dept_col"),T_("type_client_col"),T_("nom_client_col"),T_("sujet_col"),T_("adversaire_col"),T_("remarque_col"),T_("frais_col"),T_("type_affaire_col"),T_("enquete_col"),T_("date_depot_col"),T_("decision_col"),T_("date_report_col"),T_("cause_col")]
        wds  = [40,100,80,90,110,100,110,100,70,100,80,90,110,90,110]
        for i,(h,w) in enumerate(zip(hdrs,wds),1):
            self.tree.heading(i,text=h); self.tree.column(i,width=w,anchor="center")
        sb = ttk.Scrollbar(c,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left",fill="both",expand=True)
        sb.pack(side="left",fill="y")

    def on_show(self): self.charger()

    def charger(self):
        aid = db.SESSION.get("avocat_id")
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = db.query(
            "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,sujet,"
            "adversaire,remarque,frais_affaire,type_affaire,numero_enquete,"
            "date_depot_dossier,decision_finale,date,cause_romprement "
            "FROM archive WHERE avocat_id=%s",(aid,),fetch=True)
        for r in rows: self.tree.insert("","end",values=r)

    def supprimer(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Sélection","Sélectionnez une archive."); return
        if messagebox.askyesno("Confirmation","Supprimer ?"):
            cid = self.tree.item(sel[0],"values")[0]
            db.query("DELETE FROM archive WHERE id=%s AND avocat_id=%s",(cid,db.SESSION.get("avocat_id")))
            self.charger()

    def filtrer(self):
        val = simpledialog.askstring("Filtrer","Nom de client à rechercher:")
        if val:
            aid = db.SESSION.get("avocat_id")
            for i in self.tree.get_children(): self.tree.delete(i)
            rows = db.query(
                "SELECT id,autorite_judiciaire,salle_ou_departement,type_client,nom_client,sujet,"
                "adversaire,remarque,frais_affaire,type_affaire,numero_enquete,"
                "date_depot,decision_finale,date_de_rempore,cause_romprement "
                "FROM archive WHERE avocat_id=%s AND nom_client LIKE %s",(aid,f"%{val}%"),fetch=True)
            for r in rows: self.tree.insert("","end",values=r)

# ============================================================
#  ENREGISTREMENT DES PAGES
# ============================================================
pages["splash"]         = SplashPage(container)
pages["login"]          = LoginPage(container)
pages["inscription"]    = InscriptionPage(container)
pages["dashboard"]      = DashboardPage(container)
pages["consulter"]      = ConsulterPage(container)
pages["ajouter_affaire"]= AjouterAffairePage(container)
pages["clients"]        = ClientsPage(container)
pages["finances"]       = FinancesPage(container)
pages["calendrier"]     = CalendrierPage(container)
pages["archives"]       = ArchivesPage(container)

# Démarrer sur splash
show_page("splash")
root.mainloop()