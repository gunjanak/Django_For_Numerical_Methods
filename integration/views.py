from django.shortcuts import render
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sympy import symbols,sympify 

from integration.trapezoid import trapezoid_plot,trapezoidal_rule
from integration.simpson_one import simpson_one_plot, simpsons_one_rule
from integration.simpson_three import simpson_three_plot,simpsons_three_rule
from integration.gauss import gauss_two_point,gauss_three_point
from integration.romberg import romberg_integration

from integration.forms import IntegrationForm

# Create your views here.
def index(request):
    integration_fig = None
    algorithm_fig = None
    integration_result = None
    integration_method = None

    if request.method == 'POST':
        form = IntegrationForm(request.POST)
        if form.is_valid():
            try:
               
                formula_str = form.cleaned_data['formula']
                lower_limit = form.cleaned_data['lower_limit']
                upper_limit = form.cleaned_data['upper_limit']
                steps = form.cleaned_data['steps']
                integration_method = form.cleaned_data['integration_method']
                
                if(integration_method == 'gauss_two_point'):
                    print('gauss_two_point')
                    integration_result = gauss_two_point(formula_str,lower_limit,upper_limit)
                elif(integration_method == "gauss_three_point"):
                    print("gauss three point")
                    integration_result = gauss_three_point(formula_str,lower_limit,upper_limit)
                elif(integration_method == 'trapezoidal'):
                    print("trapezoidal")
                    integration_fig,algorithm_fig = trapezoid_plot(formula_str,lower_limit,
                                                            upper_limit,steps)
                    integration_result = trapezoidal_rule(formula_str,lower_limit,
                                                    upper_limit,steps)
                    
                elif(integration_method == 'simpson_one'):
                    print("Simpson's 1/3")
                    integration_fig,algorithm_fig = simpson_one_plot(formula_str,lower_limit,
                                                            upper_limit,steps)
                    integration_result = simpsons_one_rule(formula_str,lower_limit,
                                                    upper_limit,steps)
                elif(integration_method == 'simpson_three'):
                    print("Simpson's 3/8")
                    integration_fig,algorithm_fig = simpson_three_plot(formula_str,lower_limit,
                                                            upper_limit,steps)
                    integration_result = simpsons_three_rule(formula_str,lower_limit,
                                                    upper_limit,steps)
                elif(integration_method == 'Romberg_integration'):
                    print("Romberg Integration")
                    integration_result = romberg_integration(formula_str,lower_limit,upper_limit,steps)
                    
                



                context = {'form':form,
                           "formula":formula_str,
                           'integration_fig':integration_fig,
                            'algorithm_fig':algorithm_fig,
                           "integration_result":integration_result,
                           "integration_method":integration_method,}

                return render(request,'index.html',context)
            except Exception as e:
                error_message = f"Error evaluating the formula: {str(e)}"
                context = {'form':form,'error_message':error_message}
                return render(request,'index.html',context)
    else:
        form = IntegrationForm()

    context = {'form':form}
    return render(request,'index.html',context)






