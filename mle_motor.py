# -*- coding: utf-8 -*-
"""Hierarchikus Gamma-Poisson (NB) MLE illesztes, multi-start + numerikus Hessian."""

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln
import config


def extract_team_side_stats(rows, side):
    """side: 'home' vagy 'away'. Visszaadja: dict {csapat: (S, n)}."""
    stats = {}
    for row in rows:
        if side == "home":
            team = row["home_team"]
            corners = row["home_corners"]
        else:
            team = row["away_team"]
            corners = row["away_corners"]
        if team not in stats:
            stats[team] = [0.0, 0]
        stats[team][0] += corners
        stats[team][1] += 1
    return {t: (v[0], v[1]) for t, v in stats.items()}


def fit_hyperparams(S_array, n_array):
    """
    lambda_i ~ Gamma(a, b); x_ij | lambda_i ~ Poisson(lambda_i).
    Log-likelihood (additiv konstans nelkul):
        sum_i [ gammaln(a+S_i) - gammaln(a) + a*log(b) - (a+S_i)*log(b+n_i) ]
    """
    mask = n_array > 0
    S = S_array[mask]
    n = n_array[mask]

    if len(S) < config.MIN_TEAMS_FOR_FIT:
        raise ValueError(
            f"Tul keves csapat adat a hierarchikus illesztéshez ({len(S)} < {config.MIN_TEAMS_FOR_FIT})."
        )

    def neg_log_lik(log_params):
        log_a, log_b = log_params
        a = np.exp(log_a)
        b = np.exp(log_b)
        ll = np.sum(gammaln(a + S) - gammaln(a) + a * np.log(b) - (a + S) * np.log(b + n))
        return -ll

    rng = np.random.default_rng(config.RANDOM_SEED)
    best_result = None
    best_nll = np.inf

    for _ in range(config.N_MULTISTART):
        init_a = rng.uniform(0.5, 50.0)
        init_b = rng.uniform(0.5, 20.0)
        x0 = [np.log(init_a), np.log(init_b)]
        try:
            res = minimize(neg_log_lik, x0, method="L-BFGS-B")
            if res.success and np.isfinite(res.fun) and res.fun < best_nll:
                best_nll = res.fun
                best_result = res
        except Exception:
            continue

    if best_result is None:
        raise ValueError("Egyik multi-start optimalizalas sem konvergalt.")

    log_a_hat, log_b_hat = best_result.x
    a_hat = np.exp(log_a_hat)
    b_hat = np.exp(log_b_hat)

    def grad(params):
        g = np.zeros(2)
        for k in range(2):
            p_plus = params.copy(); p_plus[k] += config.HESSIAN_EPS
            p_minus = params.copy(); p_minus[k] -= config.HESSIAN_EPS
            g[k] = (neg_log_lik(p_plus) - neg_log_lik(p_minus)) / (2 * config.HESSIAN_EPS)
        return g

    base_params = np.array([log_a_hat, log_b_hat])
    hessian = np.zeros((2, 2))
    for k in range(2):
        p_plus = base_params.copy(); p_plus[k] += config.HESSIAN_EPS
        p_minus = base_params.copy(); p_minus[k] -= config.HESSIAN_EPS
        hessian[:, k] = (grad(p_plus) - grad(p_minus)) / (2 * config.HESSIAN_EPS)

    try:
        cov_log = np.linalg.inv(hessian)
        se_log_a = float(np.sqrt(max(cov_log[0, 0], 0)))
        se_log_b = float(np.sqrt(max(cov_log[1, 1], 0)))
    except np.linalg.LinAlgError:
        se_log_a, se_log_b = float("nan"), float("nan")

    return {
        "a": a_hat, "b": b_hat,
        "se_log_a": se_log_a, "se_log_b": se_log_b,
        "neg_log_lik": best_nll,
        "n_teams_used": len(S),
          }
