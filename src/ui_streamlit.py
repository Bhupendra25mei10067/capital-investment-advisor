# src/ui_streamlit.py
import streamlit as st
import pandas as pd
from engine import monte_carlo_npv, npv, irr, payback_period, profitability_index, recommend_from_sim

st.title("Capital Investment Advisor (Demo)")

with st.form("project_form"):
    name = st.text_input("Project name", "NewPressMachine")
    initial = st.number_input("Initial investment (capital outflow)", value=500000, step=1000.0)
    years = st.number_input("Lifetime (years)", value=7, min_value=1)
    rev_mean = st.number_input("Annual revenue (mean)", value=150000.0)
    rev_std = st.number_input("Annual revenue std dev", value=20000.0)
    cost_mean = st.number_input("Annual cost (mean)", value=40000.0)
    cost_std = st.number_input("Annual cost std dev", value=5000.0)
    discount_rate = st.number_input("Discount rate (decimal)", value=0.10)
    sims = st.number_input("Monte Carlo runs", value=2000, min_value=100, step=100)
    submitted = st.form_submit_button("Analyze")

if submitted:
    cashflows = [-initial] + [rev_mean - cost_mean] * int(years)
    st.subheader("Deterministic results")
    st.write("NPV:", npv(discount_rate, cashflows))
    st.write("IRR:", irr(cashflows))
    st.write("Payback:", payback_period(cashflows))
    st.write("Profitability Index:", profitability_index(discount_rate, cashflows))

    st.subheader("Monte Carlo simulation")
    sim = monte_carlo_npv(initial, int(years), rev_mean, rev_std, cost_mean, cost_std, discount_rate, int(sims), random_state=1)
    st.write("Mean NPV:", sim['npv_mean'])
    st.write("Std NPV:", sim['npv_std'])
    st.write("P(NPV>0):", sim['npv_percent_positive'])
    st.write("Recommendation:", recommend_from_sim(sim))

    st.subheader("Sample of simulated NPVs")
    sample = pd.Series(sim['npv_distribution']).sample(200)
    st.line_chart(sample)