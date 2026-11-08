# -*- coding: utf-8 -*-
"""2. ful GUI felepitese: Elemzes (MLE illesztes + mentes kozbenso naplobA)."""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

import config
import state
import mle_motor
import naplo


def build_tab_elemzes(notebook, kepernyo_szelesseg):
    wrap = kepernyo_szelesseg - 30
    ful = ttk.Frame(notebook)
    notebook.add(ful, text="Elemz")

    tk.Label(ful, text="Elemzes (MLE illesztes)", font=config.CIM_BETU,
             wraplength=wrap).pack(pady=10)

    def elemzes_lista_frissitese():
        csapatok = state.APP_STATE["common_reliable_teams"]
        if not csapatok:
            messagebox.showwarning("Figyelem",
                "Nincs tisztitott csapatlista. Eloszor vegezd el a Beolvasas "
                "es tisztitas lepest az Adatbevitel fulön!")
            return
        hazai_combo["values"] = csapatok
        vendeg_combo["values"] = csapatok
        allapot_label.config(text=f"Csapatlista frissitve ({len(csapatok)} csapat).", fg="blue")

    ttk.Button(ful, text="Csapatlista frissitese", wraplength=wrap - 40,
               command=elemzes_lista_frissitese).pack(fill="x", padx=20, pady=5)

    ttk.Label(ful, text="Hazai csapat:").pack(pady=(10, 3))
    hazai_valasztott = tk.StringVar()
    hazai_combo = ttk.Combobox(ful, textvariable=hazai_valasztott, values=[],
                                font=config.NAGY_BETU, state="readonly", height=config.LISTA_SOR_SZAM)
    hazai_combo.pack(fill="x", padx=20, pady=3, ipady=4)

    ttk.Label(ful, text="Vendeg csapat:").pack(pady=(10, 3))
    vendeg_valasztott = tk.StringVar()
    vendeg_combo = ttk.Combobox(ful, textvariable=vendeg_valasztott, values=[],
                                 font=config.NAGY_BETU, state="readonly", height=config.LISTA_SOR_SZAM)
    vendeg_combo.pack(fill="x", padx=20, pady=3, ipady=4)

    allapot_label = tk.Label(ful, text="Eloszor frissitsd a csapatlistat.",
                              font=config.KICSI_BETU, fg="black", wraplength=wrap, justify="left")
    allapot_label.pack(pady=(10, 5))

    eredmeny_label = tk.Label(ful, text="", font=config.KOZEPES_BETU, fg="green",
                               wraplength=wrap, justify="left")
    eredmeny_label.pack(pady=10)

    def elemzes_futtatasa():
        if not state.APP_STATE["prev_rows"]:
            messagebox.showwarning("Figyelem",
                "Eloszor vegezd el a Beolvasas es tisztitas lepest az Adatbevitel fulön!")
            return

        hazai = hazai_valasztott.get()
        vendeg = vendeg_valasztott.get()

        if not hazai or not vendeg:
            messagebox.showwarning("Figyelem", "Valaszd ki mindket csapatot!")
            return
        if hazai == vendeg:
            messagebox.showwarning("Figyelem", "A ket csapat nem lehet ugyanaz!")
            return

        try:
            allapot_label.config(text="MLE illesztes folyamatban...", fg="blue")
            ful.update_idletasks()

            prev_rows = state.APP_STATE["prev_rows"]
            home_stats = mle_motor.extract_team_side_stats(prev_rows, "home")
            away_stats = mle_motor.extract_team_side_stats(prev_rows, "away")

            S_home = np.array([v[0] for v in home_stats.values()])
            n_home = np.array([v[1] for v in home_stats.values()])
            S_away = np.array([v[0] for v in away_stats.values()])
            n_away = np.array([v[1] for v in away_stats.values()])

            fit_home = mle_motor.fit_hyperparams(S_home, n_home)
            fit_away = mle_motor.fit_hyperparams(S_away, n_away)

            S_hazai, n_hazai = home_stats.get(hazai, (0.0, 0))
            S_vendeg, n_vendeg = away_stats.get(vendeg, (0.0, 0))

            a_h, b_h = fit_home["a"], fit_home["b"]
            a_a, b_a = fit_away["a"], fit_away["b"]

            lambda_hazai = (a_h + S_hazai) / (b_h + n_hazai)
            post_var_hazai = (a_h + S_hazai) / (b_h + n_hazai) ** 2
            pred_sd_hazai = np.sqrt(lambda_hazai + post_var_hazai)

            lambda_vendeg = (a_a + S_vendeg) / (b_a + n_vendeg)
            post_var_vendeg = (a_a + S_vendeg) / (b_a + n_vendeg) ** 2
            pred_sd_vendeg = np.sqrt(lambda_vendeg + post_var_vendeg)

            state.APP_STATE["last_analysis"] = {
                "hazai": hazai, "vendeg": vendeg,
                "lambda_hazai": float(lambda_hazai), "sd_hazai": float(pred_sd_hazai),
                "n_hazai": int(n_hazai),
                "lambda_vendeg": float(lambda_vendeg), "sd_vendeg": float(pred_sd_vendeg),
                "n_vendeg": int(n_vendeg),
            }

            szoveg = (
                f"HAZAI ({hazai}): {lambda_hazai:.2f} +/- {pred_sd_hazai:.2f} "
                f"(n={n_hazai}, prior atlag={a_h / b_h:.2f})\n\n"
                f"VENDEG ({vendeg}): {lambda_vendeg:.2f} +/- {pred_sd_vendeg:.2f} "
                f"(n={n_vendeg}, prior atlag={a_a / b_a:.2f})\n\n"
                f"[MERVE] HOME a={a_h:.3f}, b={b_h:.3f} | AWAY a={a_a:.3f}, b={b_a:.3f}"
            )
            eredmeny_label.config(text=szoveg, fg="green")
            allapot_label.config(text="MLE illesztes sikeres.", fg="green")

        except Exception as e:
            allapot_label.config(text="Hiba tortent az elemzes soran.", fg="red")
            messagebox.showerror("Hiba", str(e))

    tk.Button(ful, text="ELEMZES\nFUTTATASA", font=("Arial", 18, "bold"),
              bg="#2196F3", fg="white", command=elemzes_futtatasa,
              wraplength=wrap - 40, justify="center", height=2).pack(
        fill="x", padx=20, pady=10)

    ttk.Label(ful, text="Bajnoksag (liga) neve:").pack(pady=(10, 3))
    liga_entry = ttk.Entry(ful, font=config.NAGY_BETU)
    liga_entry.pack(fill="x", padx=20, pady=3, ipady=4)

    def mentes():
        if state.APP_STATE["last_analysis"] is None:
            messagebox.showwarning("Figyelem", "Eloszor futtasd le az elemzest!")
            return
        liga = liga_entry.get().strip()
        if not liga:
            messagebox.showwarning("Figyelem", "Add meg a bajnoksag (liga) nevet!")
            return
        try:
            match_id = naplo.mentes_kozbenso_naplo(state.APP_STATE["last_analysis"], liga)
            allapot_label.config(text=f"Mentve a kozbenso naploba (ID: {match_id}).", fg="green")
        except Exception as e:
            messagebox.showerror("Hiba", f"Mentesi hiba:\n{e}")

    tk.Button(ful, text="MENTES KOZBENSO\nNAPLOBA", font=("Arial", 18, "bold"),
              bg="#FF9800", fg="white", command=mentes,
              wraplength=wrap - 40, justify="center", height=2).pack(fill="x", padx=20, pady=10)

    return ful
