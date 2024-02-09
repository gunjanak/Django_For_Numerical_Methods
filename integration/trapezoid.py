import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def trapezoid_plot(lower_limit,higher_limit,steps):
    height = (higher_limit - lower_limit)/steps
    x = np.arange(lower_limit,higher_limit,height)
    x = np.append(x,higher_limit)
    x = x.tolist()
    print(x)
    y = np.sin(x)
    print(y)
    print(len(x))

    #using plotly.express
    x_values = np.arange(0,3.14,0.01)
    y_values = np.sin(x_values)
    fig_express = px.line(x=x_values,y=y_values,labels={'x':'Radians','y':'y=sin(x)'},
                          title='y=sin(x)',height=800)

    for i in range(len(x)):
        fig_express.add_trace(go.Scatter(x=[x[i],x[i]],y=[0,y[i]],mode='lines',line=dict(color='red')))
    
    for i in range(len(x)-1):
        fig_express.add_trace(go.Scatter(x=[x[i],x[i+1]],y=[y[i],y[i+1]],
                                         mode='lines',line=dict(color='red')))
        # Shade the area 
        fig_express.add_trace(go.Scatter(x=[x[i],x[i],x[i+1],x[i+1]], y=[0,y[i],y[i+1], 0],
                                    fill='toself', fillcolor='rgba(255, 0, 0, 0.2)',
                                    line=dict(color='rgba(255, 255, 255, 0)')))

    

    trapezoid_fig = fig_express.to_html(full_html=False)
    return trapezoid_fig

def trapezoidal_rule(lower_limit,higher_limit,steps):
    h = (higher_limit - lower_limit) / steps
    result = (np.sin(lower_limit) + np.sin(higher_limit)) / 2.0

    for i in range(1, steps):
        result += np.sin(lower_limit + i * h)

    result *= h
    return result