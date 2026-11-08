# -*- coding: utf-8 -*-
"""Fo belepesi pont. Osszeallitja az ablakot es a fuleket a tobbi modulbol."""

import tkinter as tk
from tkinter import ttk

import config
from gui_tab1_adatbevitel import build_tab_adatbevitel
from gui_tab2_elemzes import build_tab_elemzes

root = tk.Tk()
root.title("Corner Modell")

root.update_idletasks()
kepernyo_szelesseg = root.winfo_screenwidth()
kepernyo_magassag = root.winfo_screenheight()
root.geometry(f"{kepernyo_szelesseg}x{kepernyo_magassag}+0+0")

style = ttk.Style()
style.theme_use("default")
style.configure("TCombobox", font=config.NAGY_BETU, padding=6)
style.configure("TButton", font=config.KOZEPES_BETU, padding=5)
style.configure("TLabel", font=config.KOZEPES_BETU)
style.configure("TNotebook.Tab", font=config.TAB_BETU, padding=(3, 3))
root.option_add("*TCombobox*Listbox.font", config.NAGY_BETU)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

build_tab_adatbevitel(notebook, kepernyo_szelesseg)
build_tab_elemzes(notebook, kepernyo_szelesseg)

for fulnev in ["Naplo1", "Naplo2", "Teljesitm"]:
    placeholder_ful = ttk.Frame(notebook)
    notebook.add(placeholder_ful, text=fulnev)
    tk.Label(placeholder_ful, text=f"{fulnev}\n(fejlesztes alatt)",
             font=config.KOZEPES_BETU, fg="gray").pack(expand=True)

root.mainloop()
