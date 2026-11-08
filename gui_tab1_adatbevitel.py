# -*- coding: utf-8 -*-
"""1. ful GUI felepitese: Adatbevitel."""

import os
import tkinter as tk
from tkinter import ttk, messagebox

import config
import state
import adatbevitel


def build_tab_adatbevitel(notebook, kepernyo_szelesseg):
    wrap = kepernyo_szelesseg - 30
    ful = ttk.Frame(notebook)
    notebook.add(ful, text="Adat")

    tk.Label(ful, text="Adatbevitel es tisztitas", font=config.CIM_BETU,
             wraplength=wrap).pack(pady=10)
    tk.Label(ful, text=f"Mappa: {config.FOLDER_PATH}", font=config.KICSI_BETU,
             wraplength=wrap, justify="left").pack(pady=(0, 8))

    def mappa_fajlok_listazasa():
        try:
            if not os.path.isdir(config.FOLDER_PATH):
                messagebox.showerror("Hiba", f"A mappa nem talalhato:\n{config.FOLDER_PATH}")
                return []
            fajlok = [f for f in os.listdir(config.FOLDER_PATH) if f.lower().endswith(".csv")]
            return sorted(fajlok)
        except Exception as e:
            messagebox.showerror("Hiba", f"Mappa olvasasi hiba:\n{e}")
            return []

    def mappa_frissitese():
        fajlok = mappa_fajlok_listazasa()
        elozo_combo["values"] = fajlok
        jelenlegi_combo["values"] = fajlok
        if fajlok:
            allapot_label.config(text=f"Mappa frissitve. Talalt CSV fajlok: {len(fajlok)}", fg="blue")
        else:
            allapot_label.config(text="Nincs CSV fajl a mappaban.", fg="red")

    ttk.Button(ful, text="Mappa frissitese", wraplength=wrap - 40,
               command=mappa_frissitese).pack(fill="x", padx=20, pady=5)

    ttk.Label(ful, text="Elozo szezon fajl:").pack(pady=(10, 3))
    elozo_valasztott = tk.StringVar()
    elozo_combo = ttk.Combobox(ful, textvariable=elozo_valasztott, values=[],
                                font=config.NAGY_BETU, state="readonly", height=config.LISTA_SOR_SZAM)
    elozo_combo.pack(fill="x", padx=20, pady=3, ipady=4)

    ttk.Label(ful, text="Jelenlegi szezon fajl:").pack(pady=(10, 3))
    jelenlegi_valasztott = tk.StringVar()
    jelenlegi_combo = ttk.Combobox(ful, textvariable=jelenlegi_valasztott, values=[],
                                    font=config.NAGY_BETU, state="readonly", height=config.LISTA_SOR_SZAM)
    jelenlegi_combo.pack(fill="x", padx=20, pady=3, ipady=4)

    allapot_label = tk.Label(ful, text="Nyomd meg a 'Mappa frissitese' gombot eloszor.",
                              font=config.KICSI_BETU, fg="black", wraplength=wrap, justify="left")
    allapot_label.pack(pady=(10, 5))

    eredmeny_label = tk.Label(ful, text="", font=config.KOZEPES_BETU, fg="green",
                               wraplength=wrap, justify="left")
    eredmeny_label.pack(pady=10)

    def beolvasas_es_tisztitas():
        elozo_fajl = elozo_valasztott.get()
        jelenlegi_fajl = jelenlegi_valasztott.get()

        if not elozo_fajl or not jelenlegi_fajl:
            messagebox.showwarning("Figyelem", "Valaszd ki mindket fajlt!")
            return
        if elozo_fajl == jelenlegi_fajl:
            messagebox.showwarning("Figyelem", "A ket fajl nem lehet ugyanaz!")
            return

        elozo_path = os.path.join(config.FOLDER_PATH, elozo_fajl)
        jelenlegi_path = os.path.join(config.FOLDER_PATH, jelenlegi_fajl)

        try:
            allapot_label.config(text="Beolvasas folyamatban...", fg="blue")
            ful.update_idletasks()

            prev_rows_raw = adatbevitel.read_csv_robust(elozo_path)
            curr_rows_raw = adatbevitel.read_csv_robust(jelenlegi_path)

            prev_rows_clean = adatbevitel.apply_rule_a(prev_rows_raw)
            curr_rows_clean = adatbevitel.apply_rule_a(curr_rows_raw)

            common_reliable, _, _ = adatbevitel.apply_rule_b(prev_rows_clean, curr_rows_clean)

            state.APP_STATE["prev_rows"] = prev_rows_clean
            state.APP_STATE["curr_rows"] = curr_rows_clean
            state.APP_STATE["common_reliable_teams"] = common_reliable

            szoveg = (
                f"Elozo szezon: {len(prev_rows_raw)} -> {len(prev_rows_clean)} meccs (SZABALY A utan)\n"
                f"Jelenlegi szezon: {len(curr_rows_raw)} -> {len(curr_rows_clean)} meccs (SZABALY A utan)\n"
                f"Kozos es megbizhato csapatok szama: {len(common_reliable)}"
            )
            eredmeny_label.config(text=szoveg, fg="green")
            allapot_label.config(text="Beolvasas es tisztitas sikeres.", fg="green")

        except Exception as e:
            allapot_label.config(text="Hiba tortent a beolvasas soran.", fg="red")
            eredmeny_label.config(text="")
            messagebox.showerror("Hiba", str(e))

    tk.Button(ful, text="BEOLVASAS ES\nTISZTITAS", font=("Arial", 18, "bold"),
              bg="#4CAF50", fg="white", command=beolvasas_es_tisztitas,
              wraplength=wrap - 40, justify="center", height=2).pack(
        fill="x", padx=20, pady=15)

    return ful
