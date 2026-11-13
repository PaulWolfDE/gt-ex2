import math


def get_payment_basic_linear(alpha: float, budget: float) -> float:

    if alpha < 1.0:
        return 0.0

    p = 0.5
    q = -0.5

    payout = (p * alpha + q) * budget

    return payout

def get_payment_basic_exponential(alpha: float, budget: float) -> float:

    if alpha < 1.0:
        return 0.0

    a = 1.0/(math.exp(3)-math.e)
    c = -math.e

    payout = a*(math.exp(alpha) - c) * budget

    return payout

def get_payment_basic_logarithmic(alpha: float, budget: float) -> float:

    if alpha < 1.0:
        return 0.0

    a = 1.0/math.log(3)

    payout = a * math.log(alpha) * budget

    return payout