# src/examples.py
from engine import (
    npv,
    irr,
    payback_period,
    profitability_index,
    monte_carlo_npv,
    recommend_from_sim,
)

def prompt_float(prompt, default):
    s = input(f"{prompt} [{default}]: ").strip()
    if s == "":
        return float(default)
    try:
        return float(s)
    except ValueError:
        print("Invalid number — using default.")
        return float(default)

def prompt_int(prompt, default):
    s = input(f"{prompt} [{default}]: ").strip()
    if s == "":
        return int(default)
    try:
        return int(s)
    except ValueError:
        print("Invalid integer — using default.")
        return int(default)

def demo_interactive():
    print("=== Capital Investment Advisor — interactive demo ===")
    initial = prompt_float("Initial investment (positive number)", 500000)
    years = prompt_int("Lifetime (years)", 7)
    annual_revenue = prompt_float("Annual revenue (mean)", 150000)
    annual_cost = prompt_float("Annual cost (mean)", 40000)
    discount_rate = prompt_float("Discount rate (decimal, e.g. 0.10)", 0.10)
    rev_std = prompt_float("Annual revenue std dev", 20000)
    cost_std = prompt_float("Annual cost std dev", 5000)
    sims = prompt_int("Monte Carlo runs", 3000)

    # Deterministic cashflows
    cashflows = [-initial] + [annual_revenue - annual_cost] * years

    print("\n--- Deterministic results ---")
    try:
        d_npv = npv(discount_rate, cashflows)
        d_irr = irr(cashflows)
        d_pb = payback_period(cashflows)
        d_pi = profitability_index(discount_rate, cashflows)
        print(f"NPV: {d_npv}")
        print(f"IRR: {d_irr}")
        print(f"Payback (undiscounted): {d_pb}")
        print(f"Profitability Index: {round(d_pi, 3) if d_pi is not None else 'N/A'}")
    except Exception as e:
        print("Error computing deterministic results:", e)

    print("\n--- Monte Carlo simulation ---")
    try:
        sim = monte_carlo_npv(
            initial_outflow=initial,
            years=years,
            rev_mean=annual_revenue,
            rev_std=rev_std,
            cost_mean=annual_cost,
            cost_std=cost_std,
            discount_rate=discount_rate,
            n_sims=sims,
            random_state=42
        )
        print(f"Monte Carlo mean NPV: {sim['npv_mean']}")
        print(f"P(NPV>0): {sim['npv_percent_positive']}")
        print("Recommendation:", recommend_from_sim(sim))
    except Exception as e:
        print("Error running Monte Carlo:", e)

if __name__ == "__main__":
    demo_interactive()