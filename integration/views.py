from django.shortcuts import render
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from integration.trapezoid import trapezoid_plot,trapezoidal_rule
from integration.forms import IntegrationForm

# Create your views here.

def index(request):
    return render(request,'index.html')

def trapezoidal(request):
    trapezoid_fig = None
    integration_result = None

    if request.method == 'POST':
        form = IntegrationForm(request.POST)
        if form.is_valid():
            lower_limit = form.cleaned_data['lower_limit']
            upper_limit = form.cleaned_data['upper_limit']
            steps = form.cleaned_data['steps']
            trapezoid_fig = trapezoid_fig = trapezoid_plot(lower_limit,upper_limit,steps)
            integration_result = trapezoidal_rule(lower_limit,upper_limit,steps)

    else:
        form = IntegrationForm()

    
    context = {
        'form':form,
        'trapezoid_fig':trapezoid_fig,
        'integration_result':integration_result,
    }
    return render(request,"trapezoidal.html",context)