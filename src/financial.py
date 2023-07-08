def calculate_compound_interest(principal, rate, periods):
    """
    Calculate compound interest on a monthly basis.

    Args:
        principal (float): The initial amount of money invested.
        rate (float): The annual interest rate (expressed as a decimal).
        periods (int): The number of periods the money is invested for.

    Returns:
        list: A list of values representing the amount after compound interest for each month.

    """
    amounts = []
    for _ in range(1, periods + 1):
        principal = principal * (1 + rate)
        amounts.append(principal)
    return amounts
