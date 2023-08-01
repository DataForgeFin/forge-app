"""Brazilian taxes"""


def iof(days: int):
    """
    IOF tax. Source:
    https://www.tesourodireto.com.br/blog/quais-sao-os-impostos-e-taxas-ao-investir-no-td.htm
    Input: days (int) -> days since start of investiment
    """
    if days <= 30 and days > 0:
        return (30 - days) / 30
    else:
        return 0


def ir(days: int, rate: float):
    """
    IR tax. Source:
    https://www.tesourodireto.com.br/blog/quais-sao-os-impostos-e-taxas-ao-investir-no-td.htm
    Input: days (int) -> days since start of investiment
    """
    if days <= 180 and days > 0:
        return rate * 0.225
    elif days <= 360:
        return rate * 0.2
    elif days <= 720:
        return rate * 0.175
    else:
        return rate * 0.15
