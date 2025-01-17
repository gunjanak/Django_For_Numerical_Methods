import numpy as np
from sympy import symbols, sympify, lambdify, diff

def fixed_point_iteration(formula,x0,E):
    print("This is Fixed Point Iteration")
    print("This is Bisection method")
    x = symbols('x')
    f_lambdified = lambdify(x,formula)
    error = 5000
    
    while error >E:
        x1 = f_lambdified(x0)
        error = abs((x1-x0)/x1)
        print(f"X0: {x0}")
        print(f"X1: {x1}")
        x0 = x1
    return x1


def bisection_method(formula,x1,x2,E):
    print("This is Bisection method")
    x = symbols('x')
    f_lambdified = lambdify(x,formula)
    error = 5000
    
    while error >E:
        fx1 = f_lambdified(x1)
        fx2 = f_lambdified(x2)
        print(f"fx1 : {fx1}")
        print(f"fx2 : {fx2}")
        x3 = (x1+x2)/2
        fx3 = f_lambdified(x3)
        if fx3 < 0:
            x1 = x3
        else:
            x2 = x3
        
        error = abs((x2-x1)/x2)
        print(f"X3: {x3}")
        print(f"Error: {error}")
    return x3


def false_position(formula,x1,x2,E):
    print("This is False position method")
    x = symbols('x')
    f_lambdified = lambdify(x,formula)
    error = 5000
    
    while error >E:
        fx1 = f_lambdified(x1)
        fx2 = f_lambdified(x2)
        print(f"fx1 : {fx1}")
        print(f"fx2 : {fx2}")
        x3 = x2 - ((x2-x1)*fx2)/(fx2-fx1)
        fx3 = f_lambdified(x3)
        if fx3 < 0:
            x1 = x3
        else:
            x2 = x3
        
        error = abs((x2-x1)/x2)
        print(f"X3: {x3}")
        print(f"Error: {error}")
    return x3
        
        
        
def secant_method(formula,x1,x2,E):
    print("This is Secant Method")
    # Define the symbol
    x = symbols('x')

    # Generate the lambdified function
    f_lambdified = lambdify(x, formula)


    error = 5000
    while error >E:
        
        fx1 = f_lambdified(x1)
        fx2 = f_lambdified(x2)
        print(f"fx1 : {fx1}")
        print(f"fx2 : {fx2}")

        x3 = x2 - ((x2-x1)*fx2)/(fx2-fx1)
        
        error = abs((x3-x2)/x3)
        print(f"X3: {x3}")
        print(f"Error: {error}")
        
        x1 = x2
        x2 = x3
        
    print(f"X3: {x3}")
    return x3
    
    

def newton_raphson(formula,x0,E):
 
    # Define the symbol
    x = symbols('x')

    # Generate the lambdified function
    f_lambdified = lambdify(x, formula)

    # Compute the derivative of the formula
    formula_derivative = diff(formula, x)

    # Generate the lambdified derivative
    f_derivative_lambdified = lambdify(x, formula_derivative)

    # Evaluate the function and its derivative at a specific point
    xi = x0
    output = f_lambdified(xi)
    output_derivative = f_derivative_lambdified(xi)

    # Display results
    print(f"The function: {formula}")
    print(f"The derivative: {formula_derivative}")
    print(f"f({xi}) = {output}")
    print(f"f'({xi}) = {output_derivative}")
    error = 5000
    while error>E:
        xiold = xi
        xi = xi-(f_lambdified(xi)/f_derivative_lambdified(xi))
        error = abs((xi-xiold)/xi)
        print(f"Xi: {xi}")
        print(f"Error: {error}")
        
    print(xi)
    return xi
    