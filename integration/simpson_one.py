import numpy as np
from sympy import symbols,sympify 
from scipy.optimize import curve_fit

import plotly.express as px
import plotly.graph_objects as go

def create_shaded_region(formula,x_start, x_end):
    x = symbols('x')
    x_values = np.arange(x_start,x_end,0.01)
    y_values = [float(formula.subs(x, x_val).evalf()) for x_val in x_values]
    x_shaded = np.concatenate([[x_start], x_values, [x_end]])
    y_shaded = np.concatenate([[0], y_values, [0]])
    return x_shaded, y_shaded

def create_shaded_region_quad(params,x_start,x_end):
    x_values = np.arange(x_start,x_end,0.01)
    a_fit, b_fit, c_fit = params
    y_values = quadratic_function(x_values, a_fit, b_fit, c_fit)
    x_shaded = np.concatenate([[x_start], x_values, [x_end]])
    y_shaded = np.concatenate([[0], y_values, [0]])
    return x_shaded, y_shaded

# Define the quadratic function
def quadratic_function(x, a, b, c):
    return a * x**2 + b * x + c

def quadratic_curve(x_data,y_data):
    x_curves= []
    y_curves = []
    parameters = []
    #split x_data and y_data in chunks of three
    x_data = [(x_data[i], x_data[i+1], x_data[i+2]) for i in range(0, len(x_data)-2, 2)]
    y_data = [(y_data[i], y_data[i+1], y_data[i+2]) for i in range(0, len(y_data)-2, 2)]

    # print(f"************{x_data}**************")
    # print(f"************{y_data}**************")

    for i in range(len(x_data)):
        # Use curve_fit to fit the quadratic function to the data
        params, covariance = curve_fit(quadratic_function, x_data[i], y_data[i])
        # Extract coefficients from the fit
        a_fit, b_fit, c_fit = params
        # Print the quadratic equation
        quadratic_equation = f"{a_fit}*x**2 + {b_fit}*x + {c_fit}"
        # print("Quadratic Equation:", quadratic_equation)
        # Generate x values for the curve
        x_curve = np.linspace(min(x_data[i]), max(x_data[i]), 100)

        # Calculate corresponding y values using the fitted coefficients
        y_curve = quadratic_function(x_curve, a_fit, b_fit, c_fit)
        
        x_curves.append(x_curve.tolist())
        y_curves.append(y_curve.tolist())
        parameters.append(params)
    
    return x_curves,y_curves,parameters



def simpson_one_plot(formula_str,lower_limit,higher_limit,steps):
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

    x_curves,y_curves,parameters = quadratic_curve(x,y)
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
    simpson_one_fig = fig_express.to_html(full_html=False)
    return integration_main,simpson_one_fig



def simpsons_one_rule(formula_str,lower_limit,higher_limit,steps):
    """
    Approximate the definite integral of a function using Simpson's 1/3 rule.

    Parameters:
    - f: The function to be integrated.
    - a, b: The limits of integration.
    - n: The number of subintervals. It should be an even number.

    Returns:
    - The approximate definite integral.
    """
    formula = sympify(formula_str)
    x_in = symbols('x')

    h = (higher_limit - lower_limit) / steps
    x = np.linspace(lower_limit, higher_limit, steps+1)
    y = [float(formula.subs(x_in, x_val).evalf()) for x_val in x]
    # print(x)

    result = h / 3 * (y[0] + 4 * sum(y[1:-1:2]) + 2 * sum(y[2:-2:2]) + y[-1])

    return result


