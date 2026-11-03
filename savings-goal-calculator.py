# Day 28 (2026-11-03): Savings Goal Calculator
# A small tool that tells you how long it will take to reach a savings goal.
# Useful for everyone: saving for a phone, a bike, a trip, an emergency fund,
# or any big purchase - it plans the months needed and shows the final amount.
# Uses only the Python standard library (no external libraries).

import math


def months_to_goal(goal_amount, current_savings=0.0, monthly_saving=0.0,
                   annual_interest_rate=0.0):
    """Return the number of months needed to reach a savings goal.

    goal_amount: total amount you want to save (must be > 0)
    current_savings: amount you already have saved
    monthly_saving: amount you will save each month
    annual_interest_rate: bank interest per year in percent (e.g. 5 for 5%).
        Set to 0 if you keep the money at home / no interest.

    Interest compounds monthly on the running balance.
    Raises ValueError on bad input, or if the goal can never be reached.
    """
    if goal_amount <= 0:
        raise ValueError("goal_amount must be positive")
    if current_savings < 0 or monthly_saving < 0 or annual_interest_rate < 0:
        raise ValueError("amounts and interest rate cannot be negative")
    if current_savings >= goal_amount:
        return 0

    monthly_rate = annual_interest_rate / 100.0 / 12.0

    if monthly_rate == 0:
        # No interest: simple division, rounded up to a whole month.
        if monthly_saving <= 0:
            raise ValueError("goal can never be reached: "
                             "monthly saving is 0 and no interest")
        return math.ceil((goal_amount - current_savings) / monthly_saving)

    # With interest: simulate month by month until the balance reaches the goal.
    if monthly_saving <= 0:
        raise ValueError("goal can never be reached: "
                         "monthly saving is 0 and interest alone is not "
                         "simulated here - add a monthly saving amount")
    balance = current_savings
    months = 0
    while balance < goal_amount:
        balance = balance * (1 + monthly_rate) + monthly_saving
        months += 1
        if months > 1200:  # safety cap: 100 years
            raise ValueError("goal unreachable within 100 years")
    return months


def savings_plan(goal_amount, current_savings=0.0, monthly_saving=0.0,
                 annual_interest_rate=0.0):
    """Return a dict with the full plan: months, years+months, total paid in,
    and the final balance after the last payment."""
    months = months_to_goal(goal_amount, current_savings, monthly_saving,
                            annual_interest_rate)
    monthly_rate = annual_interest_rate / 100.0 / 12.0
    balance = current_savings
    for _ in range(months):
        balance = balance * (1 + monthly_rate) + monthly_saving
    return {
        "months": months,
        "years": months // 12,
        "remaining_months": months % 12,
        "total_contributed": round(current_savings + monthly_saving * months, 2),
        "final_balance": round(balance, 2),
    }


def monthly_needed(goal_amount, current_savings, months,
                   annual_interest_rate=0.0):
    """Return the monthly saving amount needed to reach the goal in `months`."""
    if months <= 0:
        raise ValueError("months must be positive")
    if goal_amount <= 0:
        raise ValueError("goal_amount must be positive")
    if current_savings >= goal_amount:
        return 0.0
    monthly_rate = annual_interest_rate / 100.0 / 12.0
    if monthly_rate == 0:
        return math.ceil((goal_amount - current_savings) / months * 100) / 100
    future_of_current = current_savings * (1 + monthly_rate) ** months
    needed = (goal_amount - future_of_current) * monthly_rate / \
        ((1 + monthly_rate) ** months - 1)
    return math.ceil(max(needed, 0) * 100) / 100


if __name__ == "__main__":
    # Example 1: Saving for a new smartphone (150,000 taka in 12 months).
    plan = savings_plan(goal_amount=150000, current_savings=20000,
                        monthly_saving=12000)
    print("Phone savings plan:", plan)
    # -> about 11 months, then you own the phone.

    # Example 2: How much to save each month for a 300,000 taka bike in 18 months?
    print("Monthly needed for bike:",
          monthly_needed(goal_amount=300000, current_savings=50000,
                         months=18), "taka")

    # Example 3: Emergency fund of 500,000 taka with 5% yearly bank interest.
    plan3 = savings_plan(goal_amount=500000, current_savings=100000,
                         monthly_saving=15000, annual_interest_rate=5)
    print("Emergency fund plan:", plan3)
