import numpy as np
from sympy import symbols,sympify 


def euler(formula,x0,y0,h,xn):
    x, y = symbols('x y')
    steps = int((xn-x0)/h)
    xi = x0
    yi = y0
    for i in range(steps):
        initial_values = {x:xi,y:yi}
        print(initial_values)
        result = formula.subs(initial_values)
        print(f"values: {result}")
        yi = yi + h*formula.subs(initial_values)
        xi = xi+h
        print(f"xi: {xi}")
        print(f"yi: {yi}")
        
    return yi

def heun(formula,x0,y0,h,xn):
    x, y = symbols('x y')
    steps = int((xn-x0)/h)
    xi = x0
    yi = y0
    
    for i in range(steps):
        initial_values = {x:xi,y:yi}
        print(initial_values)
        m1 = formula.subs(initial_values)
        xi2 = xi+h
        yi2 = yi+m1*h
        sec_values = {x:xi2,y:yi2}
        m2 = formula.subs(sec_values)
        m = (m1+m2)/2
        yi = yi+m*h
        xi = xi+h
        print(f"xi: {xi}")
        print(f"yi: {yi}")
    return yi
    