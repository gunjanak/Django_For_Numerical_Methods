from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import FormulaInputForm
from sympy import symbols, sympify

from .ode import euler,heun,rk4

def index(request):
    return render(request,'ode_home.html')


def initial_value_view(request):
    result = None
    if request.method == "POST":
        form = FormulaInputForm(request.POST)
        if form.is_valid():
            # Extract the data from the form
            formula_str = form.cleaned_data['formula']
            initial_x = form.cleaned_data['initial_x']
            initial_y = form.cleaned_data['initial_y']
            height = form.cleaned_data['height']
            final_x = form.cleaned_data['final_x']
            method = form.cleaned_data['method']
            
            # Perform calculations (e.g., parsing formula or applying the method)
            x, y = symbols('x y')  # Define symbolic variables
            formula = sympify(formula_str)  # Convert formula string to sympy expression
            
            print(f"Formula string: {formula_str}")
            print(f"x: {initial_x}")
            print(f"y: {initial_y}")
            print(f"h: {height}")
            print(f"xn: {final_x}")
            print(method)
            print(type(method))
            if method == "Euler":
                final_y = round(euler(formula,initial_x,initial_y,height,final_x),3)
            elif method == "Heun":
                final_y = round(heun(formula,initial_x,initial_y,height,final_x),3)
                
            elif method == "RK":
                final_y = round(rk4(formula,initial_x,initial_y,height,final_x),3)
            
            
            # Placeholder: You can implement Euler, Heun, or RK methods here
            result = f"Formula: {formula}, Method: {method}, X0: {initial_x},Y0: {initial_y},\
            height:{height},Xn:{final_x},Yn:{final_y}"
            
            return render(request, 'ode_form.html', {'form': form, 'result': result})

            
    else:
        form = FormulaInputForm()
    
    return render(request, 'ode_form.html', {'form': form})
