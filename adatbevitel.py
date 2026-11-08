# -*- coding: utf-8 -*-
"""Fajlbeolvasas, SZABALY A (szezon-szivargas), SZABALY B (csapat-megbizhatosag)."""

import csv
from datetime import datetime
import config


def normalize_key(s):
    return s.strip().lower().replace(" ", "").replace("_", "").replace("-", "")


def build_header_map(fieldnames):
    header_map = {}
    normalized_fieldnames = {normalize_key(fn): fn for fn in fieldnames}
    for standard_key, alias_list in config.COLUMN_ALIASES.items():
        for alias in alias_list:
            if alias in normalized_fieldnames:
                header_map[standard_key] = normalized_fieldnames[alias]
                break
    return header_map


def parse_date_safe(date_str):
    date_str = date_str.strip()
    for fmt in config.DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def read_csv_robust(filepath):
    last_error = None
    for encoding in config.ENCODING_TRY_ORDER:
        try:
            with open(filepath, "r", encoding=encoding, newline="") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                if not fieldnames:
                    raise ValueError("Ures vagy ervenytelen CSV fejlec.")

                header_map = build_header_map(fieldnames)
                required = ["date", "home_team", "away_team", "home_corners", "away_corners"]
                missing = [r for r in required if r not in header_map]
                if missing:
                    raise ValueError(f"Hianyzo oszlopok: {missing}. Talalt fejlec: {fieldnames}")

                rows = []
                for raw_row in reader:
                    try:
                        date_val = parse_date_safe(raw_row[header_map["date"]])
                        if date_val is None:
                            continue
                        home_team = raw_row[header_map["home_team"]].strip()
                        away_team = raw_row[header_map["away_team"]].strip()
                        home_corners = float(raw_row[header_map["home_corners"]])
                        away_corners = float(raw_row[header_map["away_corners"]])
                        if not home_team or not away_team:
                            continue
                        rows.append({
                            "date": date_val, "home_team": home_team, "away_team": away_team,
                            "home_corners": home_corners, "away_corners": away_corners,
                        })
                    except (ValueError, KeyError):
                        continue

                if len(rows) == 0:
                    raise ValueError("Nulla ervenyes sor a beolvasas utan.")
                return rows

        except (UnicodeDecodeError, ValueError) as e:
            last_error = e
            continue

    raise ValueError(f"Egyik kodolas sem mukodott. Utolso hiba: {last_error}")


def apply_rule_a(rows):
    if len(rows) < 10:
        return rows
    sorted_rows = sorted(rows, key=lambda r: r["date"])
    n = len(sorted_rows)
    window = max(1, int(n * config.SEARCH_WINDOW_FRACTION))

    cut_start_idx = 0
    for i in range(min(window, n - 1)):
        gap_days = (sorted_rows[i + 1]["date"] - sorted_rows[i]["date"]).days
        if gap_days >= config.CONTAMINATION_GAP_THRESHOLD_DAYS:
            cut_start_idx = i + 1

    cut_end_idx = n
    for i in range(n - 1, max(n - 1 - window, 0), -1):
        gap_days = (sorted_rows[i]["date"] - sorted_rows[i - 1]["date"]).days
        if gap_days >= config.CONTAMINATION_GAP_THRESHOLD_DAYS:
            cut_end_idx = i

    cleaned = sorted_rows[cut_start_idx:cut_end_idx]
    return cleaned if len(cleaned) > 0 else sorted_rows


def compute_team_match_counts(rows):
    counts = {}
    for row in rows:
        counts[row["home_team"]] = counts.get(row["home_team"], 0) + 1
        counts[row["away_team"]] = counts.get(row["away_team"], 0) + 1
    return counts


def apply_rule_b(prev_rows, curr_rows):
    prev_counts = compute_team_match_counts(prev_rows)
    curr_counts = compute_team_match_counts(curr_rows)
    prev_max = max(prev_counts.values()) if prev_counts else 0
    curr_max = max(curr_counts.values()) if curr_counts else 0
    prev_reliable = {t for t, c in prev_counts.items() if c >= config.MIN_MATCH_RATIO * prev_max}
    curr_reliable = {t for t, c in curr_counts.items() if c >= config.MIN_MATCH_RATIO * curr_max}
    common_reliable = sorted(prev_reliable & curr_reliable)
    return common_reliable, prev_counts, curr_counts
