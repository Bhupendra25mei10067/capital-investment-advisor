# 📘 Capital Investment Advisor

## 🔵 1. Project Description
This project is a Python-based capital budgeting tool that evaluates investment projects using financial metrics and Monte Carlo simulation. It helps determine whether a project should be accepted or rejected based on profitability, risk, and expected return.

---

## 💰 2. Features
- 📌 Calculates essential financial metrics:
  - **NPV (Net Present Value)**
  - **IRR (Internal Rate of Return)**
  - **Payback Period**
  - **Profitability Index (PI)**
- 🎲 **Monte Carlo simulation** to measure uncertainty and risk
- 🧮 Provides **probability of positive returns**
- 🟢 Final recommendation: **ACCEPT / REJECT / BORDERLINE**

---

## 🟡 3. How to Run

### ▶️ CLI Mode
```bash
python3 src/examples.py
```

---

## 🟢 4. Requirements

Install dependencies:
```bash
pip install numpy pandas scipy
```

---

## 📘 5. Explanation of Terms (Inputs)

### 💵 Initial Investment
Money spent at the start of the project.

### 📅 Lifetime (Years)
How long the project generates cashflows.

### 💰 Annual Revenue (Mean)
Average yearly income.

### 🧾 Annual Cost (Mean)
Average yearly expenditure.

### 🔻 Discount Rate
Rate used to convert future cashflows into present value.
Entered as decimal:
- 0.10 = 10%
- If you enter **10**, system converts it to **0.10**

### 📉 Revenue Standard Deviation (Std Dev)
How much revenue fluctuates each year (risk).

### 📈 Cost Standard Deviation (Std Dev)
How much cost fluctuates each year.

### 🎲 Monte Carlo Runs
Number of random simulations to estimate risk.

---

## 🔴 6. Outputs Explanation (Results)

### 💰 NPV (Net Present Value)
Value added by the project after discounting future cashflows.
- Positive NPV → Profitable
- Negative NPV → Loss

### 📈 IRR (Internal Rate of Return)
The rate at which NPV becomes zero.
Used to compare against required rate of return.

### ⏳ Payback Period
Years required to recover the initial investment.

### 📊 Profitability Index (PI)
Present value of inflows divided by initial investment.
- PI > 1 → Acceptable
- PI < 1 → Not acceptable

### 🎲 Monte Carlo Mean NPV
Average NPV from all simulation runs.

### 🎯 Probability of Positive NPV
Percentage of simulations where the project is profitable.

### 🏁 Final Recommendation
- **ACCEPT** – high profitability and low risk
- **REJECT** – low profitability or high risk
- **BORDERLINE** – uncertain or mixed results
