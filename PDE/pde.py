import numpy as np
from sympy import symbols,sympify,lambdify


def poisson(formula,f1_x,f1_y,f2_x,f2_y,f3_x,f3_y,f4_x,f4_y):
    
    x, y = symbols('x y')
    f_lambdified = lambdify((x, y), formula)
    coefficients = [[-4,1,1,0],
                            [1,-4,0,1],
                            [1,0,-4,1],
                            [0,1,1,-4]]
    
    constants = [[f_lambdified(f1_x,f1_y)],
                         [f_lambdified(f2_x,f2_y)],
                         [f_lambdified(f3_x,f3_y)],
                         [f_lambdified(f4_x,f4_y)]]
    solution = np.linalg.solve(coefficients, constants)
    
        
    return solution