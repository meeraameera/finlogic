import math


def calculate_future_value(P, r, t, n, PMT=0):
    """
    Calculates the Future Value (FV) of an investment with periodic contributions (PMT).
    
    Arguments:
    P: Principal (Initial Deposit)
    r: Annual interest rate (as a decimal)
    t: Time in years
    n: Compounding frequency per year 
    PMT: Periodic contribution amount 
    
    Returns: 
    fv: Future Value of the investment
    total_interest: Total interest earned over the period
    """

    # Convert interest rate from percentage to decimal if needed
    if r > 1:
        r = r / 100
        
    i = r / n       # Periodic rate
    N = t * n       # Total number of periods

    if i == 0:
        # Case for 0% interest: FV is just principal + total contributions
        fv = P + (PMT * N)
        total_interest = 0
        return fv, total_interest

    # Future Value of the Principal (without contributions)
    fv_principal = P * (1 + i)**N
    
    # Future Value of an Ordinary Annuity (contributions at the end of each period)
    fv_annuity = PMT * (((1 + i)**N - 1) / i)
    
    # Total Future Value = FV of principal + FV of contributions
    fv = fv_principal + fv_annuity
    
    # Total capital invested = principal + sum of all contributions
    total_capital = P + (PMT * N)

    # Interest earned = FV - total capital invested
    total_interest = fv - total_capital
    
    return fv, total_interest


def calculate_loan_emi(P, r, t, n):
    """
    Calculates the Equal Monthly Installment (EMI) for a loan.

    Arguments:
    P: Principal (Loan Amount)
    r: Annual interest rate (as a decimal)
    t: Time in years
    n: Payment frequency per year (usually 12 for monthly)
    
    Returns: 
    emi: Regular payment amount per period
    """

    # Convert interest rate from percentage to decimal if needed
    if r > 1:
        r = r / 100

    i = r / n       # Periodic interest rate
    N = t * n       # Total number of payments

    if i == 0:
        # Case for 0% interest: simple division of principal over payments
        return P / N 
    
    # EMI formula: PMT = (P * i) / (1 - (1 + i)^-N)
    denominator = 1 - (1 + i)**(-N)
    
    if denominator == 0:
        return float('inf') 
        
    emi = (P * i) / denominator

    return emi
