import numpy as np
import plotly.graph_objs as go

from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


import numpy as np
import plotly.graph_objects as go

import numpy as np
import plotly.graph_objects as go

def newton_backward_divided_difference(x_points, y_points, x_val):
    """
    Perform Newton's Backward Interpolation and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_val (float): The x-value at which to evaluate the interpolation.

    Returns:
        tuple: The interpolated value at x_val, the backward difference table, and the Plotly figure.
    """
    # Number of points
    n = len(x_points)

    # Check if the x values are equally spaced
    h = x_points[1] - x_points[0]
    if not all(abs(x_points[i + 1] - x_points[i] - h) < 1e-9 for i in range(n - 1)):
        raise ValueError("x values must be equally spaced for Newton's Backward Interpolation.")

    # Create the backward difference table
    backward_diff = np.zeros((n, n + 1))
    backward_diff[:, 0] = x_points
    backward_diff[:, 1] = y_points

    for j in range(2, n + 1):
        for i in range(j - 1, n):
            backward_diff[i, j] = backward_diff[i, j - 1] - backward_diff[i - 1, j - 1]

    # Calculate p for interpolation
    p = (x_val - x_points[-1]) / h

    # Calculate the interpolated value using the formula
    result = backward_diff[n - 1, 1]
    term = 1.0
    for i in range(1, n):
        term *= (p + (i - 1))  # Multiply by p(p+1)(p+2)... as per the formula
        result += (term / np.math.factorial(i)) * backward_diff[n - 1, i + 1]

    # Generate interpolated values for plotting
    x_fit = np.linspace(min(x_points), max(x_points), 500)
    y_fit = []
    for xi in x_fit:
        p_fit = (xi - x_points[-1]) / h
        yi = backward_diff[n - 1, 1]
        term_fit = 1.0
        for i in range(1, n):
            term_fit *= (p_fit + (i - 1))
            yi += (term_fit / np.math.factorial(i)) * backward_diff[n - 1, i + 1]
        y_fit.append(yi)

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add the interpolation curve
    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Newton interpolation', line=dict(color='blue')))
    # Add the interpolated point
    fig.add_trace(go.Scatter(x=[x_val], y=[result], mode='markers', name=f'Interpolated Point ({x_val:.2f}, {result:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title="Newton's Backward Interpolation",
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    # Return the result, backward difference table, and figure
    return result, backward_diff, fig

# Example usage
# x_points = [1, 2, 3, 4, 5]
# y_points = [1, 4, 9, 16, 25]
# x_val = 4.5
# result, table, fig = newton_backward_interpolation(x_points, y_points, x_val)
# fig.show()


def newton_forward_divided_difference(x_points, y_points, x_val):
    """
    Perform Newton's Forward Divided Difference interpolation and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_val (float): The x-value at which to evaluate the interpolation.

    Returns:
        tuple: The interpolated value at x_val, the forward difference table, and the Plotly figure.
    """
    # Number of points
    n = len(x_points)

    # Check if the x values are equally spaced
    h = x_points[1] - x_points[0]
    if not all(abs(x_points[i + 1] - x_points[i] - h) < 1e-9 for i in range(n - 1)):
        raise ValueError("x values must be equally spaced for Newton's Forward Divided Difference.")

    # Create the forward difference table
    forward_diff = np.zeros((n, n))
    forward_diff[:, 0] = y_points

    for j in range(1, n):
        for i in range(n - j):
            forward_diff[i, j] = forward_diff[i + 1, j - 1] - forward_diff[i, j - 1]

    # Calculate the interpolated value
    result = forward_diff[0, 0]
    term = 1.0
    factorial = 1
    for i in range(1, n):
        term *= (x_val - x_points[0]) / (i * h)
        result += term * forward_diff[0, i]

    # Generate interpolated values for plotting
    x_fit = np.linspace(min(x_points), max(x_points), 500)
    y_fit = []
    for xi in x_fit:
        yi = forward_diff[0, 0]
        term = 1.0
        factorial = 1
        for i in range(1, n):
            term *= (xi - x_points[0]) / (i * h)
            yi += term * forward_diff[0, i]
        y_fit.append(yi)

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add the interpolation curve
    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Newton interpolation', line=dict(color='blue')))
    # Add the interpolated point
    fig.add_trace(go.Scatter(x=[x_val], y=[result], mode='markers', name=f'Interpolated Point ({x_val:.2f}, {result:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title="Newton's Forward Divided Difference Interpolation",
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    # Return the result, forward difference table, and figure
    return result, forward_diff, fig


# def polynomial_regression(x_points, y_points, x_in, degree=2):
#     """
#     Perform polynomial regression of the specified degree, evaluate at x_in, and plot the result using Plotly.

#     Args:
#         x_points (list or np.ndarray): X data points.
#         y_points (list or np.ndarray): Y data points.
#         x_in (float): The x-value at which to evaluate the polynomial regression.
#         degree (int): Degree of the polynomial (default is 2).

#     Returns:
#         tuple: The polynomial equation, R² score, the evaluated value at x_in, and the Plotly figure.
#     """
#     # Reshape the data
#     x_points = np.array(x_points).reshape(-1, 1)
#     y_points = np.array(y_points)

#     # Transform the data for polynomial regression (degree 2)
#     poly_features = PolynomialFeatures(degree=degree)
#     x_poly = poly_features.fit_transform(x_points)

#     # Fit the linear regression model to the polynomial-transformed data
#     model = LinearRegression()
#     model.fit(x_poly, y_points)

#     # Calculate the regression curve
#     y_fit = model.predict(x_poly)

#     # Polynomial coefficients
#     coefficients = model.coef_
#     intercept = model.intercept_

#     # Polynomial equation
#     equation = f"y = {coefficients[2]:.4f}x² + {coefficients[1]:.4f}x + {intercept:.4f}"

#     # R² score
#     r2_score = model.score(x_poly, y_points)

#     # Evaluate at x_in
#     x_in_poly = poly_features.transform([[x_in]])
#     y_in = model.predict(x_in_poly)[0]

#     # Generate data for the curve plot
#     x_fit = np.linspace(min(x_points), max(x_points), 500).reshape(-1, 1)
#     x_fit_poly = poly_features.transform(x_fit)
#     y_fit_plot = model.predict(x_fit_poly)

#     # Create the Plotly figure
#     fig = go.Figure()
#     # Add original data points
#     fig.add_trace(go.Scatter(x=x_points.flatten(), y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
#     # Add polynomial regression curve
#     fig.add_trace(go.Scatter(x=x_fit.flatten(), y=y_fit_plot, mode='lines', name=f'Polynomial Regression (Degree {degree})', line=dict(color='blue')))
#     # Add the evaluated point (x_in, y_in)
#     fig.add_trace(go.Scatter(x=[x_in], y=[y_in], mode='markers', name=f'Evaluated Point ({x_in:.2f}, {y_in:.2f})', marker=dict(color='green', size=12)))

#     # Customize the layout
#     fig.update_layout(
#         title=f'Polynomial Regression (Degree {degree})<br>{equation} (R² = {r2_score:.4f})',
#         xaxis_title='x',
#         yaxis_title='y',
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         template="plotly_white"
#     )

#     return equation, r2_score, y_in, fig




def polynomial_regression(x_points, y_points, x_in, degree=2):
    """
    Perform polynomial regression of the specified degree, evaluate at x_in, and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_in (float): The x-value at which to evaluate the polynomial regression.
        degree (int): Degree of the polynomial (default is 2).

    Returns:
        tuple: The polynomial equation, R² score, the evaluated value at x_in, the Plotly figure, and the regression table.
    """
    # Reshape the data
    x_points = np.array(x_points).reshape(-1, 1)
    y_points = np.array(y_points)

    # Transform the data for polynomial regression (degree 2)
    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(x_points)

    # Fit the linear regression model to the polynomial-transformed data
    model = LinearRegression()
    model.fit(x_poly, y_points)

    # Calculate the regression curve
    y_fit = model.predict(x_poly)

    # Polynomial coefficients
    coefficients = model.coef_
    intercept = model.intercept_

    # Polynomial equation
    equation = f"y = {coefficients[degree]:.4f}x^{degree} + {coefficients[1]:.4f}x + {intercept:.4f}"

    # R² score
    r2_score = model.score(x_poly, y_points)

    # Evaluate at x_in
    x_in_poly = poly_features.transform([[x_in]])
    y_in = model.predict(x_in_poly)[0]

    # Generate data for the curve plot
    x_fit = np.linspace(min(x_points), max(x_points), 500).reshape(-1, 1)
    x_fit_poly = poly_features.transform(x_fit)
    y_fit_plot = model.predict(x_fit_poly)

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points.flatten(), y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add polynomial regression curve
    fig.add_trace(go.Scatter(x=x_fit.flatten(), y=y_fit_plot, mode='lines', name=f'Polynomial Regression (Degree {degree})', line=dict(color='blue')))
    # Add the evaluated point (x_in, y_in)
    fig.add_trace(go.Scatter(x=[x_in], y=[y_in], mode='markers', name=f'Evaluated Point ({x_in:.2f}, {y_in:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title=f'Polynomial Regression (Degree {degree})<br>{equation} (R² = {r2_score:.4f})',
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    # Create the regression table with additional columns
    table_data = []
    for x, y in zip(x_points.flatten(), y_points):
        x2 = x ** 2
        x3 = x ** 3
        x4 = x ** 4
        xy = x * y
        x2y = x2 * y
        table_data.append({
            'x': x,
            'y': y,
            'x2': x2,
            'x3': x3,
            'x4': x4,
            'xy': xy,
            'x2y': x2y
        })

    # Add sums for each column
    sum_row = {
        'x': np.sum(x_points),
        'y': np.sum(y_points),
        'x2': np.sum(x2 for x2 in (x ** 2 for x in x_points.flatten())),
        'x3': np.sum(x3 for x3 in (x ** 3 for x in x_points.flatten())),
        'x4': np.sum(x4 for x4 in (x ** 4 for x in x_points.flatten())),
        'xy': np.sum(x * y for x, y in zip(x_points.flatten(), y_points)),
        'x2y': np.sum(x2 * y for x2, y in zip((x ** 2 for x in x_points.flatten()), y_points))
    }
    table_data.append(sum_row)

    return equation, r2_score, y_in, fig, table_data



def cubic_spline_interpolation(x_points, y_points, x_val):
    """
    Perform cubic spline interpolation and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_val (float): The x-value at which to evaluate the interpolation.

    Returns:
        tuple: The interpolated value at x_val and the Plotly figure.
    """
    # Create a cubic spline interpolator
    spline = CubicSpline(x_points, y_points)

    # Interpolated value at x_val
    result = spline(x_val)

    # Generate interpolated values for plotting
    x_fit = np.linspace(min(x_points), max(x_points), 500)
    y_fit = spline(x_fit)

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add the cubic spline interpolation curve
    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Cubic Spline Interpolation', line=dict(color='blue')))
    # Add the interpolated point
    fig.add_trace(go.Scatter(x=[x_val], y=[result], mode='markers', name=f'Interpolated Point ({x_val:.2f}, {result:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title='Cubic Spline Interpolation',
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    return result, fig




def newton_divided_difference(x_points, y_points, x_val):
    """
    Perform Newton's Central Divided Difference interpolation and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_val (float): The x-value at which to evaluate the interpolation.

    Returns:
        tuple: The interpolated value at x_val, the divided difference table, and the Plotly figure.
    """
    # Number of points
    n = len(x_points)

    # Create the divided difference table with an extra column for x values
    divided_diff = np.zeros((n, n + 1))
    divided_diff[:, 0] = x_points
    divided_diff[:, 1] = y_points

    for j in range(2, n + 1):
        for i in range(n - j + 1):
            divided_diff[i, j] = (divided_diff[i + 1, j - 1] - divided_diff[i, j - 1]) / (x_points[i + j - 1] - x_points[i])

    # Calculate the interpolated value
    result = divided_diff[0, 1]
    term = 1.0
    for i in range(1, n):
        term *= (x_val - x_points[i - 1])
        result += term * divided_diff[0, i + 1]

    # Generate interpolated values for plotting
    x_fit = np.linspace(min(x_points), max(x_points), 500)
    y_fit = []
    for xi in x_fit:
        yi = divided_diff[0, 1]
        term = 1.0
        for i in range(1, n):
            term *= (xi - x_points[i - 1])
            yi += term * divided_diff[0, i + 1]
        y_fit.append(yi)

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add the interpolation curve
    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Newton interpolation', line=dict(color='blue')))
    # Add the interpolated point
    fig.add_trace(go.Scatter(x=[x_val], y=[result], mode='markers', name=f'Interpolated Point ({x_val:.2f}, {result:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title='Newton\'s Central Divided Difference Interpolation',
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    # Return the result, divided difference table, and figure
    return result, divided_diff, fig




def lagrange_interpolation(x_points, y_points, x_val):
    """
    Perform Lagrange interpolation and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_val (float): The x-value at which to evaluate the interpolation.

    Returns:
        tuple: The interpolated value at x_val, the Plotly figure, and a table of intermediate values.
    """
    # Perform Lagrange interpolation
    n = len(x_points)
    result = 0
    table_data = []  # Store intermediate values for the table

    for i in range(n):
        term = y_points[i]
        term_details = []  # To store details of the current term
        

        for j in range(n):
            if i != j:
                factor = (x_val - x_points[j]) / (x_points[i] - x_points[j])
                term *= factor
                term_details.append(factor)
        print(f"term: {term/y_points[i]}")
        print(f"y_value: {y_points[i]}")

        table_data.append({
            'i': i,
            'term': term/y_points[i],
            'y_value': y_points[i]
        })
        result += term

    # Generate interpolated values for plotting
    x_fit = np.linspace(min(x_points), max(x_points), 500)
    y_fit = []
    for xi in x_fit:
        yi = 0
        for i in range(n):
            term = y_points[i]
            for j in range(n):
                if i != j:
                    term *= (xi - x_points[j]) / (x_points[i] - x_points[j])
                    
            
            yi += term
        y_fit.append(yi)
       

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points, y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add the interpolation curve
    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Lagrange interpolation', line=dict(color='blue')))
    # Add the interpolated point
    fig.add_trace(go.Scatter(x=[x_val], y=[result], mode='markers', name=f'Interpolated Point ({x_val:.2f}, {result:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title='Lagrange Interpolation',
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    
    

    return result,table_data,fig

# # Example usage
# x_points = [1, 2, 3]
# y_points = [4, 5, 6]
# x_val = 2.5
# result, fig, table = lagrange_interpolation(x_points, y_points, x_val)
# print(f"Interpolated value at x = {x_val}: {result}")
# print("Intermediate values:")
# for row in table:
#     print(row)

# fig.show()



def linear_regression(x_points, y_points, x_in):
    """
    Perform linear regression, evaluate at x_in, and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_in (float): The x-value at which to evaluate the linear regression.

    Returns:
        tuple: The regression equation as a string, R² score, the interpolated value at x_in, 
               the Plotly figure, and the table data with x, y, x², xy, and sums.
    """
    # Reshape the data for sklearn LinearRegression
    x_points = np.array(x_points).reshape(-1, 1)
    y_points = np.array(y_points)

    # Fit the linear regression model
    model = LinearRegression()
    model.fit(x_points, y_points)

    # Calculate the regression line
    y_fit = model.predict(x_points)

    # Equation of the line
    slope = model.coef_[0]
    intercept = model.intercept_
    equation = f"y = {slope:.4f}x + {intercept:.4f}"

    # R² score
    r2_score = model.score(x_points, y_points)

    # Evaluate at x_in
    y_in = model.predict([[x_in]])[0]

    # Generate data for the line plot
    x_fit = np.linspace(min(x_points), max(x_points), 500).reshape(-1, 1)
    y_fit_plot = model.predict(x_fit)

    # Create the Plotly figure
    fig = go.Figure()
    # Add original data points
    fig.add_trace(go.Scatter(x=x_points.flatten(), y=y_points, mode='markers', name='Data points', marker=dict(color='red', size=10)))
    # Add regression line
    fig.add_trace(go.Scatter(x=x_fit.flatten(), y=y_fit_plot, mode='lines', name='Regression Line', line=dict(color='blue')))

    # Add the evaluated point (x_in, y_in)
    fig.add_trace(go.Scatter(x=[x_in], y=[y_in], mode='markers', name=f'Evaluated Point ({x_in:.2f}, {y_in:.2f})', marker=dict(color='green', size=12)))

    # Customize the layout
    fig.update_layout(
        title=f'Linear Regression<br>{equation} (R² = {r2_score:.4f})',
        xaxis_title='x',
        yaxis_title='y',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    # Generate the table data with x, y, x², and xy
    table_data = []
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_xy = 0

    for i in range(len(x_points)):
        x_val = x_points[i][0]
        y_val = y_points[i]
        x2_val = x_val ** 2
        xy_val = x_val * y_val

        sum_x += x_val
        sum_y += y_val
        sum_x2 += x2_val
        sum_xy += xy_val

        table_data.append({
            'x': x_val,
            'y': y_val,
            'x²': x2_val,
            'xy': xy_val
        })

    # Add the sum row at the end of the table
    table_data.append({
        'x': f"Σx = {sum_x}",
        'y': f"Σy = {sum_y}",
        'x²': f"Σx² = {sum_x2}",
        'xy': f"Σxy = {sum_xy}"
    })

    return equation, r2_score, y_in, fig, table_data

