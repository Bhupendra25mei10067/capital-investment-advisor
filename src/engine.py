# src/engine.py
import numpy as np
import pandas as pd
from scipy.optimize import newton

def npv(rate, cashflows):
    """Rate as decimal, cashflows list with period 0...n (period 0 is initial outflow, negative)."""
    t = np.arange(len(cashflows))
    return np.sum(cashflows / ((1 + rate) ** t))

def irr(cashflows, guess=0.1):
    """Compute IRR using Newton method with safe fallback to bracket search."""
    # Define NPV function
    def f(r):
        return npv(r, cashflows)
    try:
        r = newton(f, guess, maxiter=200)
        return r
    except Exception:
        # bracket search fallback
        rates = np.linspace(-0.99, 1.0, 2000)
        npvs = [f(r) for r in rates]
        sign_changes = np.where(np.sign(npvs[:-1]) != np.sign(npvs[1:]))[0]
        if len(sign_changes) == 0:
            return None
        idx = sign_changes[0]
        return (rates[idx] + rates[idx+1]) / 2

def payback_period(cashflows):
    """Return undiscounted payback period (float years) or None if never paid back."""
    cum = np.cumsum(cashflows)
    if cum[-1] < 0:
        return None
    years = np.searchsorted(cum, 0.0)
    if years == 0:
        return 0.0
    prev = cum[years-1]
    fraction = -prev / (cum[years] - prev)
    return (years - 1) + fraction

def discounted_payback(cashflows, rate):
    disc_cf = [cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows)]
    return payback_period(disc_cf)

def profitability_index(rate, cashflows):
    pv_positive = sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows) if t>0)
    initial = -cashflows[0]
    if initial == 0: 
        return None
    return pv_positive / initial

# Monte Carlo simulation for uncertain annual cashflows
def monte_carlo_npv(initial_outflow, years, rev_mean, rev_std, cost_mean, cost_std, discount_rate, n_sims=5000, random_state=None):
    rng = np.random.RandomState(random_state)
    results = []
    for sim in range(n_sims):
        revs = rng.normal(loc=rev_mean, scale=rev_std, size=years)
        costs = rng.normal(loc=cost_mean, scale=cost_std, size=years)
        yearly_cf = revs - costs
        cashflows = np.concatenate(([-initial_outflow], yearly_cf))
        results.append(npv(discount_rate, cashflows))
    results = np.array(results)
    return {
        'npv_mean': results.mean(),
        'npv_std': results.std(),
        'npv_percent_positive': float((results > 0).mean()),
        'npv_percent_above_threshold': float((results > 0).mean()),  # alias
        'npv_distribution': results  # large array; can sample or save
    }

# Simple recommendation rules
def recommend_from_sim(sim_results, accept_threshold=0.6, mean_npv_min=0):
    """
    Rule:
     - Accept if percent_positive >= accept_threshold and mean NPV >= mean_npv_min
     - Reject if percent_positive < 0.3 or mean_npv < 0
     - Else Borderline
    """
    ppos = sim_results['npv_percent_positive']
    mn = sim_results['npv_mean']
    if ppos >= accept_threshold and mn >= mean_npv_min:
        return "ACCEPT"
    if ppos < 0.30 or mn < 0:
        return "REJECT"
    return "BORDERLINE"