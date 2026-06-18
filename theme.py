# ============================================================
#  theme.py — Thème moderne CaseCraft
# ============================================================
import tkinter as tk
from tkinter import ttk
import datetime

BG        = "#0D1B2A"
BG2       = "#1B2A3B"
BG3       = "#162032"
ACCENT    = "#C0392B"
ACCENT2   = "#E74C3C"
CYAN      = "#1ABC9C"
TEXT      = "#ECF0F1"
TEXT2     = "#95A5A6"
BORDER    = "#2C3E50"
WHITE     = "#FFFFFF"
SUCCESS   = "#27AE60"

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_SUB    = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_LABEL  = ("Segoe UI", 11, "bold")

def apply_base(root):
    root.configure(bg=BG)

def style_treeview(cols_conf):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("M.Treeview",
        background=BG2, foreground=TEXT,
        rowheight=30, fieldbackground=BG2,
        borderwidth=0, font=FONT_BODY)
    style.configure("M.Treeview.Heading",
        background=BG3, foreground=CYAN,
        font=FONT_LABEL, relief="flat")
    style.map("M.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", WHITE)])

def make_header(parent, title, back_cmd=None):
    h = tk.Frame(parent, bg=BG3, height=58)
    h.pack(fill="x")
    h.pack_propagate(False)
    tk.Label(h, text="⚖  CaseCraft", bg=BG3, fg=CYAN,
             font=("Segoe UI", 15, "bold")).pack(side="left", padx=18)
    tk.Label(h, text=f"/ {title}", bg=BG3, fg=TEXT2,
             font=FONT_BODY).pack(side="left")
    dat = datetime.datetime.now()
    tk.Label(h, text="{:%d/%m/%Y  %H:%M}".format(dat),
             bg=BG3, fg=TEXT2, font=FONT_SMALL).pack(side="right", padx=18)
    if back_cmd:
        b = tk.Button(h, text="← Retour", bg=ACCENT, fg=WHITE,
                      font=FONT_SMALL, relief="flat",
                      activebackground=ACCENT2, cursor="hand2",
                      padx=10, pady=3, command=back_cmd)
        b.pack(side="right", padx=6, pady=12)
    return h

def make_sidebar(parent, items):
    sb = tk.Frame(parent, bg=BG3, width=200)
    sb.pack(fill="y", side="left")
    sb.pack_propagate(False)
    tk.Label(sb, text="NAVIGATION", bg=BG3, fg=TEXT2,
             font=("Segoe UI", 8, "bold")).pack(pady=(18, 6), padx=12, anchor="w")
    for icon, label, cmd in items:
        row = tk.Frame(sb, bg=BG3, cursor="hand2")
        row.pack(fill="x", pady=1)
        lbl = tk.Label(row, text=f"  {icon}  {label}",
                       bg=BG3, fg=TEXT, font=("Segoe UI", 11),
                       anchor="w", pady=9, padx=8)
        lbl.pack(fill="x")
        for w in (row, lbl):
            w.bind("<Enter>", lambda e, r=row, l=lbl: (r.config(bg=BORDER), l.config(bg=BORDER)))
            w.bind("<Leave>", lambda e, r=row, l=lbl: (r.config(bg=BG3),   l.config(bg=BG3)))
            w.bind("<Button-1>", lambda e, c=cmd: c())
    return sb

def card(parent, **kw):
    return tk.Frame(parent, bg=BG2,
                    highlightbackground=BORDER,
                    highlightthickness=1, **kw)

def lbl(parent, text, size=11, bold=False, color=TEXT, bg=None):
    bg = bg if bg else (parent.cget("bg") if hasattr(parent, 'cget') else BG)
    return tk.Label(parent, text=text, bg=bg, fg=color,
                    font=("Segoe UI", size, "bold" if bold else "normal"))

def entry(parent, w=28, show=""):
    e = tk.Entry(parent, bg=BG3, fg=TEXT, insertbackground=TEXT,
                 relief="flat", font=FONT_BODY, width=w, show=show,
                 highlightbackground=BORDER, highlightthickness=1,
                 highlightcolor=CYAN)
    return e

def combo(parent, values, w=28):
    style = ttk.Style()
    style.configure("M.TCombobox", fieldbackground=BG3,
                    background=BG3, foreground=TEXT,
                    selectbackground=ACCENT, selectforeground=WHITE)
    c = ttk.Combobox(parent, values=values, width=w,
                     style="M.TCombobox", font=FONT_BODY, state="readonly")
    return c

def btn(parent, text, cmd=None, color=ACCENT, hover=ACCENT2, w=18, fg=WHITE):
    b = tk.Button(parent, text=text, bg=color, fg=fg,
                  font=FONT_LABEL, relief="flat",
                  activebackground=hover, activeforeground=WHITE,
                  cursor="hand2", width=w, pady=5, command=cmd)
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def section_title(parent, text, bg=None):
    bg = bg or BG2
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=text, bg=bg, fg=CYAN, font=FONT_SUB).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=8, pady=9)
    return f