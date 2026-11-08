# -*- coding: utf-8 -*-
"""Kozos beallitasok es konstansok. Ide semmilyen fuggvenylogika nem kerul."""

FOLDER_PATH = "/storage/emulated/0/totalcorner/"
INTERMEDIATE_LOG_PATH = FOLDER_PATH + "naplo_kozbenso.csv"
MAIN_LOG_PATH = FOLDER_PATH + "naplo_fo.csv"

CONTAMINATION_GAP_THRESHOLD_DAYS = 60
SEARCH_WINDOW_FRACTION = 0.33
MIN_MATCH_RATIO = 0.5
ENCODING_TRY_ORDER = ["utf-8", "utf-8-sig", "cp1250", "latin1"]

COLUMN_ALIASES = {
    "date": ["date", "matchdate", "match_date", "datum", "day", "gamedate"],
    "home_team": ["home", "hometeam", "home_team", "hazai", "hazaicsapat", "homeside"],
    "away_team": ["away", "awayteam", "away_team", "vendeg", "vendegcsapat", "awayside"],
    "home_corners": ["homecorners", "home_corners", "hc", "hazaiszoglet", "homecorner"],
    "away_corners": ["awaycorners", "away_corners", "ac", "vendegszoglet", "awaycorner"],
}

DATE_FORMATS = [
    "%Y-%m-%d", "%Y.%m.%d", "%d.%m.%Y", "%d/%m/%Y",
    "%Y-%m-%d %H:%M", "%d.%m.%Y %H:%M", "%m/%d/%Y",
]

RANDOM_SEED = 42
N_MULTISTART = 8
HESSIAN_EPS = 1e-4
MIN_TEAMS_FOR_FIT = 3

NAGY_BETU = ("Arial", 18)
KOZEPES_BETU = ("Arial", 16)
KICSI_BETU = ("Arial", 13)
CIM_BETU = ("Arial", 20, "bold")
TAB_BETU = ("Arial", 11)
LISTA_SOR_SZAM = 6
