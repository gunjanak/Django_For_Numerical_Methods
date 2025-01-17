from django.shortcuts import render
from .forms import InterpolationForm
from .interpolation import (lagrange_interpolation, newton_divided_difference,cubic_spline_interpolation,
                            linear_regression,polynomial_regression)
import plotly.io as pio

def interpolation_view(request):
    if request.method == 'POST':
        form = InterpolationForm(request.POST)
        if form.is_valid():
            # Extract form data
            num_points = int(request.POST.get('num_points'))
            algorithm = request.POST.get('algorithm')
            x_values = [float(request.POST.get(f'x_{i}')) for i in range(1, num_points + 1)]
            y_values = [float(request.POST.get(f'y_{i}')) for i in range(1, num_points + 1)]
            x_in = float(request.POST.get('x_in'))

            if algorithm == "cdd":
                y_out,figure = newton_divided_difference(x_values,y_values,x_in)
            elif algorithm == "lagrange":
                # Perform interpolation
                y_out, figure = lagrange_interpolation(x_values, y_values, x_in)
            elif algorithm == "cubic_spline":
                y_out,figure = cubic_spline_interpolation(x_values, y_values, x_in)
            
            elif algorithm == "linear":
                y_out,_,__,figure = linear_regression(x_values, y_values, x_in)
            
            elif algorithm == "polynomial":
                y_out,_,__,figure = polynomial_regression(x_values,y_values,x_in)
                

            # Convert the Plotly figure to JSON
            plot_json = pio.to_json(figure)

            # Prepare the result
            result = {
                'X': x_values,
                'Y': y_values,
                'Algorithm': algorithm,
                'X_in': x_in,
                'Y_out': y_out,
                'plot_json': plot_json,
            }

            return render(request, 'interpolation.html', {'form': form, 'result': result})

    # Display the empty form
    form = InterpolationForm()
    return render(request, 'interpolation.html', {'form': form})