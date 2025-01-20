from django.shortcuts import render
from .forms import InterpolationForm
from .interpolation import (lagrange_interpolation, newton_divided_difference,cubic_spline_interpolation,
                            linear_regression,polynomial_regression,newton_forward_divided_difference,
                            newton_backward_divided_difference)
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
            print(x_values)
            print(y_values)

            divided_diff = None
            table_data = None
            regression_table = None
            if algorithm == "cdd":
                y_out,divided_diff,figure = newton_divided_difference(x_values,y_values,x_in)
            elif algorithm == "fdd":
                y_out,divided_diff,figure = newton_forward_divided_difference(x_values,y_values,x_in)
            elif algorithm == "bdd":
                y_out,divided_diff,figure = newton_backward_divided_difference(x_values,y_values,x_in)
                
            elif algorithm == "lagrange":
                # Perform interpolation
                y_out,regression_table,figure = lagrange_interpolation(x_values, y_values, x_in)
            elif algorithm == "cubic_spline":
                y_out,figure = cubic_spline_interpolation(x_values, y_values, x_in)
            
            elif algorithm == "linear":
                y_out,_,__,figure,regression_table = linear_regression(x_values, y_values, x_in)
                print(regression_table)
            
            elif algorithm == "polynomial":
                y_out,_,__,figure,regression_table = polynomial_regression(x_values,y_values,x_in)
                

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
                'divided_difference_table':divided_diff,
                'table_data':table_data,
                'regression_table':regression_table,
            }

            return render(request, 'interpolation.html', {'form': form, 'result': result})

    # Display the empty form
    form = InterpolationForm()
    return render(request, 'interpolation.html', {'form': form})
