# -*- coding: utf-8 -*-
"""Fo belepesi pont. Osszeallitja az ablakot es a fuleket a tobbi modulbol."""

import tkinter as tk
from tkinter import ttk

import config
from gui_tab1_adatbevitel import build_tab_adatbevitel
from gui_tab2_elemzes import build_tab_elemzes

root = tk.Tk()
root.title("Corner Modell - Pydroid3 App")

root.update_idletasks()
kepernyo_szelesseg = root.winfo_screenwidth()
kepernyo_magassag = root.winfo_screenheight()
root.geometry(f"{kepernyo_szelesseg}x{kepernyo_magassag}+0+0")

style = ttk.Style()
style.theme_use("default")
style.configure("TCombobox", font=config.NAGY_BETU, padding=6)
style.configure("TButton", font=config.NAGY_BETU, padding=8)
style.configure("TLabel", font=config.KOZEPES_BETU)
style.configure("TNotebook.Tab", font=config.KICSI_BETU, padding=(6, 4))
root.option_add("*TCombobox*Listbox.font", config.NAGY_BETU)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

build_tab_adatbevitel(notebook, kepernyo_szelesseg)
build_tab_elemzes(notebook, kepernyo_szelesseg)

for fulnev in ["Kozbenso naplo", "Fo naplo", "Modell teljesitmeny"]:
    placeholder_ful = ttk.Frame(notebook)
    notebook.add(placeholder_ful, text=fulnev)
    tk.Label(placeholder_ful, text=f"{fulnev}\n(fejlesztes alatt)",
             font=config.KOZEPES_BETU, fg="gray").pack(expand=True)

root.mainloop()
