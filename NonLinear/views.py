from django.shortcuts import render
from sympy import symbols, sympify

from .forms import NonlinearEquationForm

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
            
            
            # Example processing logic (customize as needed)
            result = {
                'formula': formula,
                'method': method,
                'x0': x0,
                'xn': xn,
                'error': error,
            }
            return render(request, 'nonlinear.html', {'form':form,'result': result})
    else:
        form = NonlinearEquationForm()
    
    return render(request, 'nonlinear.html', {'form': form})
