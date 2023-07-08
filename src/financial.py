def calculate_compound_interest(principal, rate, time):
    """
    Calculate compound interest on a monthly basis.

    Args:
        principal (float): The initial amount of money invested.
        rate (float): The annual interest rate (expressed as a decimal).
        time (int): The number of months the money is invested for.

    Returns:
        list: A list of values representing the amount after compound interest for each month.

    """
    monthly_rate = rate / 12

    amounts = []
    for _ in range(1, time + 1):
        principal = principal * (1 + monthly_rate)
        amounts.append(principal)
    return amounts
