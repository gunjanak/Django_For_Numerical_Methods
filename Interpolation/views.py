from django.shortcuts import render
from .forms import InterpolationForm

def interpolation_view(request):
    if request.method == 'POST':
        form = InterpolationForm(request.POST)
        if form.is_valid():
            # Handle form data
            num_points = int(request.POST.get('num_points'))
            algorithm = request.POST.get('algorithm')
            x_values = [float(request.POST.get(f'x_{i}')) for i in range(1, num_points + 1)]
            y_values = [float(request.POST.get(f'y_{i}')) for i in range(1, num_points + 1)]

            # Pass data to interpolation logic (this is where you'd compute results)
            results = f"form: {form}, Algorithm: {algorithm}, X: {x_values}, Y: {y_values}"
            result = {
                'X': x_values,
                'Y':y_values,
                'Algorithm': algorithm,
                
            }

            return render(request, 'interpolation.html', {'form':form,'result': result})

    # Display the form
    form = InterpolationForm()
    return render(request, 'interpolation.html', {'form': form})
