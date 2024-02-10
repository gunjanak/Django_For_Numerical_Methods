from django.shortcuts import render
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sympy import symbols,sympify 

from integration.trapezoid import trapezoid_plot,trapezoidal_rule
from integration.forms import IntegrationForm, FormulaEvaluationForm

# Create your views here.





def index(request):
    if request.method == 'POST':
        form = FormulaEvaluationForm(request.POST)
        if form.is_valid():
            formula_str = form.cleaned_data['formula']
            x_value = form.cleaned_data['x_value']

            try:
                x,y = symbols('x y')
                formula = sympify(formula_str)
                result = formula.subs(x,x_value)

                #Numeric evaluation using numpy
                result_numeric = float(result.evalf())
                context = {'form':form,"formula":formula_str,'x_value':x_value,'result':result_numeric}
                return render(request,'index.html',context)
            except Exception as e:
                error_message = f"Error evaluating the formula: {str(e)}"
                context = {'form':form,'error_message':error_message}
                return render(request,'index.html',context)
    else:
        form = FormulaEvaluationForm()

    context = {'form':form}
    return render(request,'index.html',context)

def trapezoidal(request):
    integration_fig = None
    trapezoid_fig = None
    integration_result = None

    if request.method == 'POST':
        form = IntegrationForm(request.POST)
        if form.is_valid():
            lower_limit = form.cleaned_data['lower_limit']
            upper_limit = form.cleaned_data['upper_limit']
            steps = form.cleaned_data['steps']
            integration_fig,trapezoid_fig = trapezoid_plot(lower_limit,upper_limit,steps)
            integration_result = trapezoidal_rule(lower_limit,upper_limit,steps)
          

    else:
        form = IntegrationForm()

    
    context = {
        'form':form,
        'integration_fig':integration_fig,
        'trapezoid_fig':trapezoid_fig,
        'integration_result':integration_result,
    }
    return render(request,"trapezoidal.html",context)