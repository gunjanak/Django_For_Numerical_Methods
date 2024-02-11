from django.shortcuts import render
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sympy import symbols,sympify 

from integration.trapezoid import trapezoid_plot,trapezoidal_rule
from integration.simpson_one import simpson_one_plot, simpsons_one_rule
from integration.simpson_three import simpson_three_plot,simpsons_three_rule

from integration.forms import (IntegrationForm, FormulaEvaluationForm,
                               SimpsonOneForm,SimpsonThreeForm)

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = FormulaEvaluationForm(request.POST)
        if form.is_valid():
            formula_str = form.cleaned_data['formula']
            x_value = form.cleaned_data['x_value']

            try:
                x = symbols('x')
                formula = sympify(formula_str)
                result = formula.subs(x,x_value)
                #Numeric evaluation using numpy
                result_numeric = float(result.evalf())
                print(result_numeric)

                #Generate plot 
                x_values = np.arange(x_value-3,x_value+3,0.01)
                y_values = [float(formula.subs(x, x_val).evalf()) for x_val in x_values]
                print(formula)
                fig_express = px.line(x=x_values,y=y_values,
                           title=formula_str,height=800)
                fig_express.update_layout(title_x=0.5, title_y=0.95, title_text=f"y={formula_str}")
                # Change font size of x and y axis labels
                fig_express.update_xaxes(title_font=dict(size=58),tickfont=dict(size=24))
                fig_express.update_yaxes(title_font=dict(size=58),tickfont=dict(size=24))
                fig_express_fig = fig_express.to_html(full_html=False)

                context = {'form':form,"formula":formula_str,'x_value':x_value,
                           'result':result_numeric,'plot':fig_express_fig}
                

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
            try:
                formula_str = form.cleaned_data['formula']
                lower_limit = form.cleaned_data['lower_limit']
                upper_limit = form.cleaned_data['upper_limit']
                steps = form.cleaned_data['steps']
                integration_fig,trapezoid_fig = trapezoid_plot(formula_str,lower_limit,
                                                            upper_limit,steps)
                integration_result = trapezoidal_rule(formula_str,lower_limit,
                                                    upper_limit,steps)
                context = {
                    'form':form,
                    'integration_fig':integration_fig,
                    'trapezoid_fig':trapezoid_fig,
                    'integration_result':integration_result,
                }
                return render(request,"trapezoidal.html",context)

            except Exception as e:
                error_message = f"Error evaluating the formula: {str(e)}"
                context = {'form':form,'error_message':error_message}
                return render(request,'trapezoidal.html',context)
          

    else:
        form = IntegrationForm()

    
    context = {
        'form':form
        }
    return render(request,"trapezoidal.html",context)




def simpson_one(request):
    integration_fig = None
    simpson_one_fig = None
    integration_result = None

    if request.method == 'POST':
        form = SimpsonOneForm(request.POST)
        if form.is_valid():
            try:
                formula_str = form.cleaned_data['formula']
                lower_limit = form.cleaned_data['lower_limit']
                upper_limit = form.cleaned_data['upper_limit']
                steps = form.cleaned_data['steps']
                integration_fig,simpson_one_fig = simpson_one_plot(formula_str,lower_limit,
                                                            upper_limit,steps)
                integration_result = simpsons_one_rule(formula_str,lower_limit,
                                                    upper_limit,steps)
                context = {
                    'form':form,
                    'integration_fig':integration_fig,
                    'simpson_one_fig':simpson_one_fig,
                    'integration_result':integration_result,
                }
                return render(request,"simpson_one.html",context)

            except Exception as e:
                error_message = f"Error evaluating the formula: {str(e)}"
                context = {'form':form,'error_message':error_message}
                return render(request,'simpson_one.html',context)
          

    else:
        form = SimpsonOneForm()

    
    context = {
        'form':form
        }
    return render(request,"simpson_one.html",context)



def simpson_three(request):
    integration_fig = None
    simpson_three_fig = None
    integration_result = None

    if request.method == 'POST':
        form = SimpsonThreeForm(request.POST)
        if form.is_valid():
            try:
                formula_str = form.cleaned_data['formula']
                lower_limit = form.cleaned_data['lower_limit']
                upper_limit = form.cleaned_data['upper_limit']
                steps = form.cleaned_data['steps']
                integration_fig,simpson_three_fig = simpson_three_plot(formula_str,lower_limit,
                                                            upper_limit,steps)
                integration_result = simpsons_three_rule(formula_str,lower_limit,
                                                    upper_limit,steps)
                context = {
                    'form':form,
                    'integration_fig':integration_fig,
                    'simpson_three_fig':simpson_three_fig,
                    'integration_result':integration_result,
                }
                return render(request,"simpson_three.html",context)

            except Exception as e:
                error_message = f"Error evaluating the formula: {str(e)}"
                context = {'form':form,'error_message':error_message}
                return render(request,'simpson_three.html',context)
          

    else:
        form = SimpsonThreeForm()

    
    context = {
        'form':form
        }
    return render(request,"simpson_three.html",context)