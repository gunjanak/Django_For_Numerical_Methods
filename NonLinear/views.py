from django.shortcuts import render
from sympy import symbols, sympify,lambdify

from .forms import NonlinearEquationForm
from .nonlinear import (newton_raphson,secant_method,false_position,
                        bisection_method,fixed_point_iteration)

def nonlinear_view(request):
    if request.method == 'POST':
        try:
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
                table = None
                
                if method == "newton_raphson":
                    output,table = newton_raphson(formula,x0,error)
                    output = round(output,3)
                elif method == "secant":
                    output,table = secant_method(formula,x0,xn,error)
                    output = round(output,3)
                
                elif method == "fixed_point":
                    output,table = fixed_point_iteration(formula,x0,error)
                    output = round(output,3)
                    
                
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
                        output,table = false_position(formula,x0,xn,error)
                        output = round(output,3)
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
                        output,table = bisection_method(formula,x0,xn,error)
                        output = round(output,3)
                        
                    
                # Example processing logic (customize as needed)
                result = {
                    'formula': formula,
                    'method': method,
                    'x0': x0,
                    'xn': xn,
                    'error': error,
                    'output':output,
                    'table':table,
                    
                }
                print(f"table: {table}")
                return render(request, 'nonlinear.html', {'form':form,'result': result})
        except Exception as e:
            error_message = f"Error evaluating the formula: {str(e)}"
            print(error_message)
            context = {'form':form,'error_message':error_message}
            return render(request,'nonlinear.html',context)
    else:
        form = NonlinearEquationForm()
    
    return render(request, 'nonlinear.html', {'form': form})
