import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from financial_logic import calculate_future_value, calculate_loan_emi


# ---------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------
st.set_page_config(layout="wide", page_title="FinLogic")
st.title("FinLogic: Calculator & Learn")
st.markdown(
    """Explore how your money grows with **Compound Interest** and understand how loans are repaid through **Amortization**."""
)
st.divider()


# ---------------------------------------------------------------
# Sidebar: Inputs
# ---------------------------------------------------------------
st.sidebar.header("Calculation Inputs")
input_method = st.sidebar.toggle("Use Manual Entry", value=False)

# Interest Rate and Time
if not input_method:
    r_input = st.sidebar.slider("Annual Interest Rate (%)", 0.0, 20.0, 5.0, 0.1)
    t = st.sidebar.slider("Time in Years", 1, 50, 10)
else:
    r_input = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.01)
    t = st.sidebar.number_input("Time in Years", min_value=1, max_value=100, value=10, step=1)

r = r_input / 100  

# Compounding / Payment frequency
n = st.sidebar.selectbox(
    "Compounding/Payment Frequency",
    [1, 2, 4, 12, 365],
    index=3,
    format_func=lambda x: f"{x} ({'Monthly' if x==12 else 'Annually' if x==1 else 'Daily' if x==365 else 'Quarterly'})"
)

# Monthly / Yearly toggle for charts
show_monthly = st.sidebar.checkbox("Show Monthly Breakdown (for FV)", value=False)


# ---------------------------------------------------------------
# Page Mode Selection
# ---------------------------------------------------------------
mode = st.radio("Select Calculator Mode:", ('Future Value (Savings)', 'Loan Repayment (Debt)'), horizontal=True)


# ---------------------------------------------------------------
# Future Value / Savings Mode
# ---------------------------------------------------------------
if mode == 'Future Value (Savings)':
    st.header("Future Value & Compound Interest")

    # Education Section
    with st.expander("Learn: How Savings Growth Works"):
        st.write("""
        **Future Value (FV)** shows how your money grows over time using **Compound Interest**.
        You earn interest not just on your principal but also on the interest accumulated.
        """)
        st.latex(r"FV = P(1 + \frac{r}{n})^{nt} + PMT \times \frac{(1 + \frac{r}{n})^{nt} - 1}{\frac{r}{n}}")
        st.write("""
        * **P**: Initial Principal  
        * **r**: Annual Interest Rate  
        * **n**: Compounding Frequency  
        * **t**: Time (Years)  
        * **PMT**: Periodic Contribution
        """)

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("Initial Principal ($)", min_value=0.0, value=10000.0, step=1000.0,
                            help="The starting amount you deposit")
    with col2:
        PMT = st.number_input("Periodic Contribution ($)", min_value=0.0, value=100.0, step=10.0,
                              help="Extra contribution added each period")

    # Compute FV and Interest
    fv, total_interest = calculate_future_value(P, r, t, n, PMT)
    total_capital = P + (PMT * t * n)

    m1, m2, m3 = st.columns(3)
    m1.metric("Final Future Value", f"${fv:,.2f}")
    m2.metric("Total Interest Earned", f"${total_interest:,.2f}")
    m3.metric("Total Capital Invested", f"${total_capital:,.2f}")

    # Generate Yearly or Monthly Balances
    if show_monthly:
        periods = t * 12
        balances = [calculate_future_value(P, r, month/12, 12, PMT)[0] for month in range(1, periods+1)]
        capitals = [P + PMT*month for month in range(1, periods+1)]
        x_axis = list(range(1, periods+1))
        x_label = "Months"
    else:
        balances = [calculate_future_value(P, r, year, n, PMT)[0] for year in range(1, t+1)]
        capitals = [P + PMT*year*n for year in range(1, t+1)]
        x_axis = list(range(1, t+1))
        x_label = "Years"

    # Plot FV vs Contributions
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_axis, y=balances, mode='lines+markers', name='Total Value',
                             line=dict(color='#2ecc71', width=3),
                             hovertemplate=f"{x_label}: %{{x}}<br>Total Value: $%{{y:,.2f}}<extra></extra>"))
    fig.add_trace(go.Scatter(x=x_axis, y=capitals, mode='lines+markers', name='Principal Invested',
                             line=dict(color='#3498db', dash='dash'),
                             hovertemplate=f"{x_label}: %{{x}}<br>Capital: $%{{y:,.2f}}<extra></extra>"))
    st.plotly_chart(fig, use_container_width=True)

    # Bar chart showing contributions vs interest earned
    interest_earned = [balances[i] - capitals[i] for i in range(len(balances))]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=x_axis, y=capitals, name='Contributions', marker_color='#3498db'))
    fig2.add_trace(go.Bar(x=x_axis, y=interest_earned, name='Interest Earned', marker_color='#2ecc71'))
    fig2.update_layout(barmode='stack', xaxis_title=x_label, yaxis_title='Amount ($)')
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------------
# Loan / Debt Mode
# ---------------------------------------------------------------
elif mode == 'Loan Repayment (Debt)':
    st.header("Loan Repayment & EMI")

    # Education Section
    with st.expander("Learn: How is a Loan Payment Calculated?"):
        st.write("""
        **Amortization** shows how each loan payment is split between interest and principal.
        Early payments mostly cover interest, while later payments reduce the principal faster.
        """)
        st.latex(r"EMI = \frac{P \times \frac{r}{n}}{1 - (1 + \frac{r}{n})^{-nt}}")
        st.write("Tip: Understanding this helps plan mortgages and loans effectively.")

    # Input Loan Principal
    P_loan = st.number_input("Loan Principal ($)", min_value=1000.0, value=250000.0, step=10000.0,
                             help="The total amount you borrow")

    # EMI Calculation
    emi = calculate_loan_emi(P_loan, r, t, n)
    total_payments = emi * t * n
    total_interest_paid = total_payments - P_loan

    c1, c2, c3 = st.columns(3)
    c1.metric("Regular Payment (EMI)", f"${emi:,.2f}")
    c2.metric("Total Payments", f"${total_payments:,.2f}")
    c3.metric("Total Interest Paid", f"${total_interest_paid:,.2f}")

    # Pie chart for principal vs interest
    fig = go.Figure(data=[go.Pie(labels=['Principal', 'Interest'],
                                 values=[P_loan, total_interest_paid],
                                 hole=.4,
                                 marker_colors=['#2ecc71', '#e74c3c'])])
    st.plotly_chart(fig, use_container_width=True)

