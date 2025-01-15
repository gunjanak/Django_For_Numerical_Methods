import numpy as np
from sympy import symbols,sympify,lambdify


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

def rk4(formula,x0,y0,h,xn):
    x, y = symbols('x y')
    steps = int((xn-x0)/h)
    xi = x0
    yi = y0
    for i in range(steps):
        initial_values = {x:xi,y:yi}
        print(initial_values)
        m1 = formula.subs(initial_values)
        xi2 = xi+(h/2)
        yi2 = yi+m1*(h/2)
        sec_values = {x:xi2,y:yi2}
        m2 = formula.subs(sec_values)
        
        xi3 = xi+(h/2)
        yi3 = yi+m2*(h/2)
        sec_values = {x:xi3,y:yi3}
        m3 = formula.subs(sec_values)
        
        xi4 = xi+h
        yi4 = yi+m3*h
        sec_values = {x:xi4,y:yi4}
        m4 = formula.subs(sec_values)
        
        m = (m1+2*m2+2*m3+m4)/6
        yi = yi+m*h
        xi = xi+h
        print(f"xi: {xi}")
        print(f"yi: {yi}")
    return yi


def second_order_ode(formula,x0,y0,z0,h,xn):
    x, y, z = symbols('x y z')
    f_lambdified = lambdify((x, y, z), formula)
    steps = int((xn-x0)/h)
    xi = x0
    yi = y0
    zi = z0
    for i in range(steps):
        m1y = zi
        m1z = f_lambdified(xi,yi,zi)
        m2y = zi + h*m1z
        xtemp = xi+h
        ytemp = yi + h*m1y
        ztemp = zi + h*m1z
        print(f"xtemp: {xtemp}")
        print(f"ytemp: {ytemp}")
        print(f"ztemp: {ztemp}")
        m2z = f_lambdified(xtemp,ytemp,ztemp)
        print(f"m1y: {m1y}")
        print(f"m1z: {m1z}")
        print(f"m2y: {m2y}")
        print(f"m2z: {m2z}")
        my = (m1y+m2y)/2
        mz = (m1z+m2z)/2
        print(f"my: {my}")
        print(f"mz: {mz}")
        
        
        yi = yi+my*h
        zi = zi + mz*h
        xi = xi+h
        print(f"xi: {xi}")
        print(f"yi: {yi}")
        print(f"zi: {zi}")
    
    return yi
    
    
    
    