import numpy as np
import plotly.graph_objs as go

from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def polynomial_regression(x_points, y_points, x_in, degree=2):
    """
    Perform polynomial regression of the specified degree, evaluate at x_in, and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_in (float): The x-value at which to evaluate the polynomial regression.
        degree (int): Degree of the polynomial (default is 2).

    Returns:
        tuple: The polynomial equation, R² score, the evaluated value at x_in, and the Plotly figure.
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
    equation = f"y = {coefficients[2]:.4f}x² + {coefficients[1]:.4f}x + {intercept:.4f}"

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

    return equation, r2_score, y_in, fig


def linear_regression(x_points, y_points, x_in):
    """
    Perform linear regression, evaluate at x_in, and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_in (float): The x-value at which to evaluate the linear regression.

    Returns:
        tuple: The regression equation as a string, R² score, the interpolated value at x_in, and the Plotly figure.
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

    return equation, r2_score, y_in, fig


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
        tuple: The interpolated value at x_val and the Plotly figure.
    """
    # Number of points
    n = len(x_points)

    # Create the divided difference table
    divided_diff = np.zeros((n, n))
    divided_diff[:, 0] = y_points

    for j in range(1, n):
        for i in range(n - j):
            divided_diff[i, j] = (divided_diff[i + 1, j - 1] - divided_diff[i, j - 1]) / (x_points[i + j] - x_points[i])

    # Calculate the interpolated value
    result = divided_diff[0, 0]
    term = 1.0
    for i in range(1, n):
        term *= (x_val - x_points[i - 1])
        result += term * divided_diff[0, i]

    # Generate interpolated values for plotting
    x_fit = np.linspace(min(x_points), max(x_points), 500)
    y_fit = []
    for xi in x_fit:
        yi = divided_diff[0, 0]
        term = 1.0
        for i in range(1, n):
            term *= (xi - x_points[i - 1])
            yi += term * divided_diff[0, i]
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

    return result, fig



def lagrange_interpolation(x_points, y_points, x_val):
    """
    Perform Lagrange interpolation and plot the result using Plotly.

    Args:
        x_points (list or np.ndarray): X data points.
        y_points (list or np.ndarray): Y data points.
        x_val (float): The x-value at which to evaluate the interpolation.

    Returns:
        tuple: The interpolated value at x_val and the Plotly figure.
    """
    # Perform Lagrange interpolation
    n = len(x_points)
    result = 0
    for i in range(n):
        term = y_points[i]
        for j in range(n):
            if i != j:
                term *= (x_val - x_points[j]) / (x_points[i] - x_points[j])
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

    return result, fig
