import numpy as np
from sympy import symbols,sympify 

def gauss_two_point(formula_str,lower_limit,upper_limit):
    formula = sympify(formula_str)
    x_in = symbols('x')
    # Gauss points and weights for two-point quadrature
    x = np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
    w = np.array([1, 1])

    # Map points from interval [-1, 1] to [a, b]
    x_mapped = 0.5 * (upper_limit - lower_limit) * x + 0.5 * (upper_limit + lower_limit)
   

    # Calculate the integral using the Gauss quadrature formula
    y = [float(formula.subs(x_in, x_val).evalf()) for x_val in x_mapped]
    integral = 0.5 * (upper_limit - lower_limit) * np.dot(w,y)

    return integral

def gauss_three_point(formula_str,lower_limit,upper_limit):
    formula = sympify(formula_str)
    x_in = symbols('x')
    # Gauss points and weights for three-point quadrature
    x = np.array([-np.sqrt(3/5), 0, np.sqrt(3/5)])
    w = np.array([5/9, 8/9, 5/9])

    # Map points from interval [-1, 1] to [a, b]
    x_mapped = 0.5 * (upper_limit - lower_limit) * x + 0.5 * (upper_limit + lower_limit)

    y = [float(formula.subs(x_in, x_val).evalf()) for x_val in x_mapped]
    # Calculate the integral using the Gauss quadrature formula
    integral = 0.5 * (upper_limit - lower_limit) * np.dot(w,y)

    return integral

