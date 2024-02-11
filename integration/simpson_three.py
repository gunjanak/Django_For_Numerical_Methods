import numpy as np
from sympy import symbols,sympify 
from scipy.optimize import curve_fit

import plotly.express as px
import plotly.graph_objects as go

# Define the quadratic function
def cubic_function(x, a, b, c,d):
    return a * x**3 + b * x**2 + c*x+d


def create_shaded_region(formula,x_start, x_end):
    x = symbols('x')
    x_values = np.arange(x_start,x_end,0.01)
    y_values = [float(formula.subs(x, x_val).evalf()) for x_val in x_values]
    x_shaded = np.concatenate([[x_start], x_values, [x_end]])
    y_shaded = np.concatenate([[0], y_values, [0]])
    return x_shaded, y_shaded

def create_shaded_region_quad(params,x_start,x_end):
    x_values = np.arange(x_start,x_end,0.01)
    a_fit, b_fit, c_fit,d_fit = params
    y_values = cubic_function(x_values, a_fit, b_fit, c_fit,d_fit)
    x_shaded = np.concatenate([[x_start], x_values, [x_end]])
    y_shaded = np.concatenate([[0], y_values, [0]])
    return x_shaded, y_shaded

def cubic_curve(x_data,y_data):
    x_curves= []
    y_curves = []
    parameters = []
    #split x_data and y_data in chunks of three
    x_data = [(x_data[i], x_data[i+1], x_data[i+2],x_data[i+3]) for i in range(0, len(x_data)-1, 3)]
    y_data = [(y_data[i], y_data[i+1], y_data[i+2],y_data[i+3]) for i in range(0, len(y_data)-1, 3)]

    # print(f"************{x_data}**************")
    # print(f"************{y_data}**************")

    for i in range(len(x_data)):
        # Use curve_fit to fit the quadratic function to the data
        params, covariance = curve_fit(cubic_function, x_data[i], y_data[i])
        # Extract coefficients from the fit
        a_fit, b_fit, c_fit,d_fit = params
        # Print the quadratic equation
        cubic_equation = f"{a_fit}*x**3 + {b_fit}*x**2 + {c_fit}*c*x + {d_fit}"
        # print("Cubic Equation:",cubic_equation)
        
        # Generate x values for the curve
        x_curve = np.linspace(min(x_data[i]), max(x_data[i]), 100)

        # Calculate corresponding y values using the fitted coefficients
        y_curve = cubic_function(x_curve, a_fit, b_fit, c_fit,d_fit)
        
        x_curves.append(x_curve.tolist())
        y_curves.append(y_curve.tolist())
        parameters.append(params)
    
    return x_curves,y_curves,parameters



def simpson_three_plot(formula_str,lower_limit,higher_limit,steps):
    formula = sympify(formula_str)

    x_in = symbols('x')

    #using plotly.express
    x_values = np.arange(lower_limit-1,higher_limit+1,0.01)
    y_values = [float(formula.subs(x_in, x_val).evalf()) for x_val in x_values]
    fig_express = px.line(x=x_values,y=y_values,
                          title=f'y={formula_str}',height=800)
    
    # Define the shaded region between x=lower_limit and x=upper_limit
    x_shaded, y_shaded = create_shaded_region(formula,lower_limit,higher_limit)
    # Add shaded region between the curve and x-axis
    fig_express.add_trace(go.Scatter(x=x_shaded, y=y_shaded, fill='toself', 
                                              fillcolor='rgba(0,100,80,0.2)', 
                                              name='Shaded Area'))
    fig_express.update_layout(title_x=0.5, title_y=0.95, title_text=f'y={formula_str}')
    # Change font size of x and y axis labels
    fig_express.update_xaxes(title_font=dict(size=30),tickfont=dict(size=20))
    fig_express.update_yaxes(title_font=dict(size=30),tickfont=dict(size=20))
    fig_express.update_layout(title_font=dict(size=30))


    fig_express_integration =go.Figure(fig_express)

    #Showing and shading how simpson's 1/3 work
    height = (higher_limit - lower_limit)/steps
    x = np.arange(lower_limit,higher_limit,height)
    x = np.append(x,higher_limit)
    x = x.tolist()
    # print(f"**********{x}*****************")
    y = [float(formula.subs(x_in, x_val).evalf()) for x_val in x]
    # print(f"**********{y}*****************")

    x_curves,y_curves,parameters = cubic_curve(x,y)
    # print(f"x_curves: {x_curves}")
    # print(f"parameters: {parameters}")
    for i in range(len(x_curves)):
        fig_express.add_trace(go.Scatter(x=x_curves[i],y=y_curves[i],
                                         mode='lines',line=dict(color='yellow')))
        
        # Define the shaded region between x=lower_limit and x=upper_limit
        x_shaded, y_shaded = create_shaded_region_quad(parameters[i],x_curves[i][0],x_curves[i][-1])
        # Add shaded region between the curve and x-axis
        fig_express.add_trace(go.Scatter(x=x_shaded, y=y_shaded, fill='toself', 
                                                fillcolor='rgba(255,100,0,0.2)', 
                                                name='Shaded Area'))

    

    
    integration_main = fig_express_integration.to_html(full_html=False)
    # simpson_one_fig = fig_express.to_html(full_html=False)
    simpson_three_fig = fig_express.to_html(full_html=False)
    return integration_main,simpson_three_fig


def simpsons_three_rule(formula_str,lower_limit,higher_limit,steps):
    """
    Calculate the definite integral of the function using Simpson's 3/8 Rule.

    Parameters:
    - formula: The function to integrate.
    - lower_limit: The lower limit of integration.
    - upper_limit: The upper limit of integration.
    - steps: The number of subintervals (must be a multiple of 3).

    Returns:
    - The approximate integral value.
    """
    formula = sympify(formula_str)
    x_in = symbols('x')

    if steps % 3 != 0:
        raise ValueError("Number of subintervals (n) must be a multiple of 3.")

    h = (higher_limit - lower_limit) / steps
    result = float(formula.subs(x_in,higher_limit).evalf()) + float(formula.subs(x_in,lower_limit).evalf())

    for i in range(1, steps):
        x = lower_limit + i * h
        weight = 3 if i % 3 == 0 else 3 if i % 3 == 1 else 2
        result += weight * float(formula.subs(x_in,x).evalf())

    return (3 * h / 8) * result