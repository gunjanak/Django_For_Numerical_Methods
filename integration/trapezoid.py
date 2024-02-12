import numpy as np
from sympy import symbols,sympify 
import plotly.express as px
import plotly.graph_objects as go



def create_shaded_region(formula,x_start, x_end):
    x = symbols('x')
    x_values = np.arange(x_start,x_end,0.01)
    y_values = [float(formula.subs(x, x_val).evalf()) for x_val in x_values]
    x_shaded = np.concatenate([[x_start], x_values, [x_end]])
    y_shaded = np.concatenate([[0], y_values, [0]])
    return x_shaded, y_shaded



def trapezoid_plot(formula_str,lower_limit,higher_limit,steps):
    formula = sympify(formula_str)

    x_in = symbols('x')
    

    height = (higher_limit - lower_limit)/steps
    x = np.arange(lower_limit,higher_limit,height)
    x = np.append(x,higher_limit)
    x = x.tolist()
    # print(x)
    y = [float(formula.subs(x_in, x_val).evalf()) for x_val in x]
    # print(y)
    # print(len(x))

    #using plotly.express
    x_values = np.arange(lower_limit-0.9,higher_limit+1,0.01)
    print("******************")
    y_values = [float(formula.subs(x_in, x_val).evalf()) for x_val in x_values]
    
    print(y_values)
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

    for i in range(len(x)):
        fig_express.add_trace(go.Scatter(x=[x[i],x[i]],y=[0,y[i]],mode='lines',line=dict(color='red')))
    
    for i in range(len(x)-1):
        fig_express.add_trace(go.Scatter(x=[x[i],x[i+1]],y=[y[i],y[i+1]],
                                         mode='lines',line=dict(color='red')))
        # Shade the area 
        fig_express.add_trace(go.Scatter(x=[x[i],x[i],x[i+1],x[i+1]], y=[0,y[i],y[i+1], 0],
                                    fill='toself', fillcolor='rgba(255, 0, 0, 0.2)',
                                    line=dict(color='rgba(255, 255, 255, 0)')))

    
    integration_main = fig_express_integration.to_html(full_html=False)
    trapezoid_fig = fig_express.to_html(full_html=False)
    return integration_main,trapezoid_fig

def trapezoidal_rule(formula_str,lower_limit,higher_limit,steps):
    formula = sympify(formula_str)
    x_in = symbols('x')
    h = (higher_limit - lower_limit) / steps
    result = (float(formula.subs(x_in,lower_limit).evalf()) + float(formula.subs(x_in,higher_limit).evalf())) / 2.0

    for i in range(1, steps):
        result += float(formula.subs(x_in,lower_limit + i * h).evalf())


    result *= h
    return result