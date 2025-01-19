import numpy as np
from sympy import symbols, sympify, lambdify, diff

def fixed_point_iteration(formula,x0,E):
    print("This is Fixed Point Iteration")
    x = symbols('x')
    f_lambdified = lambdify(x,formula)
    error = 5000
    table = []
    iteration = 0
    while error >E:
        iteration += 1
        x1 = f_lambdified(x0)
        error = abs((x1-x0)/x1)
        table.append({
            'iteration': iteration,
            'xn': x0,
            'xn+1': x1,
            'error': error
        })
        x0 = x1
    return x1,table


def bisection_method(formula,x1,x2,E):
    print("This is Bisection method")
    x = symbols('x')
    f_lambdified = lambdify(x,formula)
    error = 5000
    iteration = 0
    table = []
    while error >E:
        iteration += 1
        fx1 = f_lambdified(x1)
        fx2 = f_lambdified(x2)
        print(f"fx1 : {fx1}")
        print(f"fx2 : {fx2}")
        x3 = (x1+x2)/2
        fx3 = f_lambdified(x3)
        table_dic = {
            'iteration': iteration,
            'x1': x1,
            'fx1':fx1,
            'x2':x2,
            'fx2':fx2,
            'x3':x3,
            'fx3':fx3,
            
        }
        
        if fx3 < 0:
            x1 = x3
        else:
            x2 = x3
        
        error = abs((x2-x1)/x2)
        print(f"X3: {x3}")
        print(f"Error: {error}")
        table_dic["Error"] = error
        table_dic = {key: round(value, 4) if isinstance(value, (int, float)) else value for key, value in table_dic.items()}
        
        table.append(table_dic)
        
    return x3,table


def false_position(formula,x1,x2,E):
    print("This is False position method")
    x = symbols('x')
    f_lambdified = lambdify(x,formula)
    error = 5000
    iteration = 0
    table = []
    x3old = 5000
    while error >E:
        iteration += 1
        fx1 = f_lambdified(x1)
        fx2 = f_lambdified(x2)
        print(f"fx1 : {fx1}")
        print(f"fx2 : {fx2}")
        x3 = x1 - ((x2-x1)*fx1)/(fx2-fx1)
        fx3 = f_lambdified(x3)
        table_dic = {
            'iteration': iteration,
            'x1': x1,
            'fx1':fx1,
            'x2':x2,
            'fx2':fx2,
            'x3':x3,
            'fx3':fx3,
        }
        
        if fx3 < 0:
            x1 = x3
        else:
            x2 = x3
        
        error = abs((x3-x3old)/x3)
        x3old = x3
        print(f"X3: {x3}")
        print(f"Error: {error}")
        table_dic["Error"] = error
        table_dic = {key: round(value, 4) if isinstance(value, (int, float)) else value for key, value in table_dic.items()}
        
        table.append(table_dic)
    return x3,table
        
        
        
def secant_method(formula,x1,x2,E):
    print("This is Secant Method")
    # Define the symbol
    x = symbols('x')

    # Generate the lambdified function
    f_lambdified = lambdify(x, formula)


    error = 5000
    iteration = 0
    table = []
    while error >E:
        iteration += 0
        
        fx1 = f_lambdified(x1)
        fx2 = f_lambdified(x2)
        print(f"fx1 : {fx1}")
        print(f"fx2 : {fx2}")

        x3 = x2 - ((x2-x1)*fx2)/(fx2-fx1)
        
        error = abs((x3-x2)/x3)
        print(f"X3: {x3}")
        print(f"Error: {error}")
        table_dic = {
            'iteration': iteration,
            'x1': x1,
            'fx1':fx1,
            'x2':x2,
            'fx2':fx2,
            'x3':x3,
            'error':error
        }
        
        x1 = x2
        x2 = x3
        table_dic = {key: round(value, 4) if isinstance(value, (int, float)) else value for key, value in table_dic.items()}
        
        table.append(table_dic)
        
    print(f"X3: {x3}")
    return x3,table
    
    

def newton_raphson(formula,x0,E):
    print("Inside Newton Raphson")
 
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
    table = []
    iteration = 0
    while error>E:
        iteration += 1
        xiold = xi
        xi = xi-(f_lambdified(xi)/f_derivative_lambdified(xi))
        error = abs((xi-xiold)/xi)
        print(f"Xi: {xi}")
        print(f"Error: {error}")
        table_dic = {
            'iteration': iteration,
            'xiold': xiold,
            'fx1old':f_lambdified(xi),
            'derivative_x1old':f_derivative_lambdified(xi),
            'xi':xi,
            'error':error
        }
        table_dic = {key: round(value, 4) if isinstance(value, (int, float)) else value for key, value in table_dic.items()}
        
        table.append(table_dic)
        
    print(xi)
    return xi,table
    