import numpy as np
from sympy import symbols,sympify 


def romberg_integration(formula_str,lower_limit,upper_limit,steps):
    formula = sympify(formula_str)
    x_in = symbols('x')


    """
    Perform Romberg integration on the given function.

    Parameters:
    - func: The function to integrate.
    - a: Lower limit of integration.
    - b: Upper limit of integration.
    - n: Number of iterations.

    Returns:
    - The estimated integral value.
    """
    h = upper_limit - lower_limit

    r = [[(h / 2) * (float(formula.subs(x_in,lower_limit).evalf()) + float(formula.subs(x_in,upper_limit).evalf()))]]

    for i in range(1, steps + 1):
        h /= 2
        summation = sum(float(formula.subs(x_in,lower_limit + k * h).evalf()) for k in range(1, 2 ** i, 2))
        row = [0.5 * r[i - 1][0] + h * summation]

        for j in range(1, i + 1):
            term = row[j - 1] + (row[j - 1] - r[i - 1][j - 1]) / (4 ** j - 1)
            row.append(term)

        r.append(row)

    return r[steps][steps]