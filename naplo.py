# -*- coding: utf-8 -*-
"""Kozbenso naplo kezelese (mentes). A 3. fulnel bovul majd olvasas/frissites fuggvennyel."""

import csv
import os
from datetime import datetime
import config


def mentes_kozbenso_naplo(analysis, liga):
    """
    analysis: dict a last_analysis-bol (hazai, vendeg, lambda_hazai, sd_hazai, stb.)
    liga: string, a bajnoksag neve.
    Visszaadja az uj sor match_id-jat.
    """
    match_id = datetime.now().strftime("%Y%m%d%H%M%S")
    file_exists = os.path.isfile(config.INTERMEDIATE_LOG_PATH)

    with open(config.INTERMEDIATE_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "match_id", "datum", "liga", "hazai_csapat", "vendeg_csapat",
                "pred_hazai_szoglet", "pred_hazai_sd",
                "pred_vendeg_szoglet", "pred_vendeg_sd",
                "tenyleges_hazai_szoglet", "tenyleges_vendeg_szoglet", "lezarva",
            ])
        writer.writerow([
            match_id, datetime.now().strftime("%Y-%m-%d"), liga,
            analysis["hazai"], analysis["vendeg"],
            round(analysis["lambda_hazai"], 3), round(analysis["sd_hazai"], 3),
            round(analysis["lambda_vendeg"], 3), round(analysis["sd_vendeg"], 3),
            "", "", "nem",
        ])
    return match_id
