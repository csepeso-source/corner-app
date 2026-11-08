# -*- coding: utf-8 -*-
"""
Globalis, futasideju allapot. NEM beegetett adat - minden futtataskor
ujraszamolt ertekekkel toltodik fel. A dict mutable, igy minden modul
ugyanarra a peldanyra hivatkozik, ha 'import state'-et hasznal.
"""

APP_STATE = {
    "prev_rows": [],
    "curr_rows": [],
    "common_reliable_teams": [],
    "last_analysis": None,
}
