from django.shortcuts import render
import numpy as np
from sympy import symbols, sympify

from .pde import poisson
from .forms import LaplaceForm,PoissonForm

# Create your views here.
def index(request):
    return render(request,'pde_home.html')


def poisson_view(request):
    result = None
    if request.method == "POST":
        form = PoissonForm(request.POST)
        if form.is_valid():
            formula_str = form.cleaned_data['formula']
            f1_x = form.cleaned_data['f1_x']
            f1_y = form.cleaned_data['f1_y']
            
            f2_x = form.cleaned_data['f2_x']
            f2_y = form.cleaned_data['f2_y']
            
            f3_x = form.cleaned_data['f3_x']
            f3_y = form.cleaned_data['f3_y']
            
            f4_x = form.cleaned_data['f4_x']
            f4_y = form.cleaned_data['f4_y']
            
            formula = sympify(formula_str)
            
            solution = poisson(formula,f1_x,f1_y,f2_x,f2_y,f3_x,f3_y,f4_x,f4_y)
            
            result = {
                'f1':solution[0][0],
                'f2':solution[1][0],
                'f3':solution[2][0],
                'f4':solution[3][0],
            }
            
            return render(request, 'poisson_form.html', {'form': form, 'result': result})
            
    else:
        form = PoissonForm()
        
    return render(request, 'poisson_form.html', {'form': form})
    
            
            
def laplace_view(request):
    result = None
    if request.method == "POST":
        form = LaplaceForm(request.POST)
        if form.is_valid():
            # Extract the data from the form
            top = form.cleaned_data['top']
            left = form.cleaned_data['left']
            right = form.cleaned_data['right']
            bottom = form.cleaned_data['bottom']
            
            print(f"Top: {top}")
            print(f"Left: {left}")
            print(f"Right: {right}")
            print(f"Bottom: {bottom}")
            coefficients = [[-4,1,1,0],
                            [1,-4,0,1],
                            [1,0,-4,1],
                            [0,1,1,-4]]
            constants = [[-(top+left)],
                         [-(top+right)],[-(left+bottom)],[-(bottom+right)]]
            print(coefficients)
            print(constants)

            # Solve the system of linear equations
            solution = np.linalg.solve(coefficients, constants)
            print(solution)
            result = {
                'f1':solution[0][0],
                'f2':solution[1][0],
                'f3':solution[2][0],
                'f4':solution[3][0],
            }
            return render(request, 'laplace_form.html', {'form': form, 'result': result})

            
    else:
        form = LaplaceForm()
    
    return render(request, 'laplace_form.html', {'form': form})