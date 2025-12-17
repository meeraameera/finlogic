# finlogic

An **interactive financial education and analysis tool** designed to explain complex financial formulas through real-time visualization and dual-mode calculation.

---

## Problem Statement

Financial literacy is often hindered by calculators that provide answers without explaining the underlying logic. Users struggle to understand how variables such as compounding frequency, interest rates, or loan duration exponentially affect long-term wealth accumulation or debt levels.

---

## Project Goal

The goal of **FinLogic** is to bridge the gap between raw financial mathematics and user understanding. By combining interactive inputs with educational explanations, the tool enables users to explore **“what-if” scenarios** while learning standard industry formulas for wealth growth and debt amortization.

---

## Technical Approach

### Core Financial Logic
- Developed a modular Python backend (`financial_logic.py`) implementing algebraic formulas for:
  - **Future Value (FV)**
  - **Equated Monthly Installments (EMI)**
- Handled edge cases such as **0% interest rates** 
- Ensured **dual-use functionality** for monthly or annual compounding/payment schedules.

### Dynamic Input System
- Implemented a **dual-input toggle** (Slider vs. Manual Entry) for flexibility.
- Used `st.sidebar` to manage shared variables (`r`, `t`, `n`), ensuring consistent state across calculator modes.

### Interactive Visualizations
- Integrated **Plotly Graph Objects** for dynamic growth curves and debt breakdown charts.
- Engineered iterative balance calculations to display **year-by-year or month-by-month compound growth**, rather than static start/end values.
- Added **hover tooltips** to display exact balances, contributions, and interest at each period.

### Educational Integration
- Embedded **LaTeX-rendered equations** for formal financial formulas (`FV`, `EMI`).
- Used `st.expander` components to provide *just-in-time* financial definitions and conceptual explanations.
- Separated visual elements for **Principal vs. Interest** to enhance conceptual clarity.

---

## Impact

- **Instant Feedback:**  
  Users see immediate visual updates when variables change, illustrating the effect of compound interest.

- **Improved Accuracy:**  
  Manual input mode supports precise decimal values, important for real-world financial calculations like mortgage rates.

- **Conceptual Clarity:**  
  Visual separation of **Principal vs. Interest** helps users understand the true long-term cost of borrowing and the effect of regular contributions on savings growth.

- **Enhanced Engagement:**  
  Interactive charts encourage experimentation and exploration of what-if scenarios.

---

## Key Challenges Faced

- **Conceptual Understanding of Financial Mathematics:**  
  - *Challenge:* At the start of the project, I had a limited understanding of time value of money concepts such as compounding, periodic interest rates, and loan amortization. 
  - *Resolution:* I independently researched financial theory through documentation and practical examples. As I implemented the formulas from first principles, the calculator itself became a learning tool, reinforcing my understanding through real-time visualization and experimentation.

- **Formula Transparency:**  
  - *Challenge:* Text-based explanations were insufficient for communicating complex financial relationships.  
  - *Resolution:* Integrated **LaTeX-rendered equations** to explicitly show how variables such as periodic rate (`i`) and total number of periods (`N`) influence the final outcome.

- **Formula Transparency:**  
  - *Challenge:* Representing growth over multiple periods without cluttering the interface.
  - *Resolution:* Designed year-by-year or month-by-month charts with hover details, stacked bars for contributions vs interest, and interactive pie charts for debt breakdown.

---

## Installation & Execution

- Clone the repository
- Create and activate a virtual environment
- Install required dependencies
- Run the Streamlit app
  - `streamlit run app.py`

