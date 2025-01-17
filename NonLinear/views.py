from django.shortcuts import render
from sympy import symbols, sympify,lambdify

from .forms import NonlinearEquationForm
from .nonlinear import (newton_raphson,secant_method,false_position,
                        bisection_method,fixed_point_iteration)

def nonlinear_view(request):
    if request.method == 'POST':
        form = NonlinearEquationForm(request.POST)
        if form.is_valid():
            # Process the form data
            formula = form.cleaned_data['formula']
            method = form.cleaned_data['integration_method']
            x0 = form.cleaned_data.get('x0', None)
            xn = form.cleaned_data.get('xn', None)
            error = form.cleaned_data['error']
            formula = sympify(formula)
            print(f"Formula: {formula}")
            print(f"Method: {method}")
            print(f"x0: {x0}")
            print(f"xn: {xn}")
            print(f"Error: {error}")
            
            if method == "newton_raphson":
                output = round(newton_raphson(formula,x0,error),3)
            elif method == "secant":
                output = round(secant_method(formula,x0,xn,error),3)
            
            elif method == "fixed_point":
                output = round(fixed_point_iteration(formula,x0,error),3)
            
            elif method == "false_position":
                x = symbols('x')
                # Generate the lambdified function
                f_lambdified = lambdify(x, formula)
                fx0 = f_lambdified(x0)
                fxn = f_lambdified(xn)
                if fx0 >0:
                    message = "functional value at x0 should be negative"
                    return render(request, 'nonlinear.html', {'form':form,'message':message})
                elif fxn <0:
                    message = "functional value of xn should be positive"
                    return render(request, 'nonlinear.html', {'form':form,'message':message})
                else:
                    output = round(false_position(formula,x0,xn,error),3)
            elif method == "bisection":
                x = symbols('x')
                # Generate the lambdified function
                f_lambdified = lambdify(x, formula)
                fx0 = f_lambdified(x0)
                fxn = f_lambdified(xn)
                if fx0 >0:
                    message = "functional value at x0 should be negative"
                    return render(request, 'nonlinear.html', {'form':form,'message':message})
                elif fxn <0:
                    message = "functional value of xn should be positive"
                    return render(request, 'nonlinear.html', {'form':form,'message':message})
                else:
                    output = round(bisection_method(formula,x0,xn,error),3)
                    
                
            # Example processing logic (customize as needed)
            result = {
                'formula': formula,
                'method': method,
                'x0': x0,
                'xn': xn,
                'error': error,
                'output':output,
                
            }
            return render(request, 'nonlinear.html', {'form':form,'result': result})
    else:
        form = NonlinearEquationForm()
    
    return render(request, 'nonlinear.html', {'form': form})
