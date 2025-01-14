from django.shortcuts import render
import numpy as np


from .forms import MatrixForm


# Create your views here.
def index(request):
    return render(request,'linear_algebra_home.html')


def matrix_view(request):
    if request.method == 'POST':
        form = MatrixForm(request.POST)
        if form.is_valid():
            matrix_size = int(form.cleaned_data['matrix_size'])
            matrix_values = np.zeros(shape=(matrix_size,matrix_size))

            # Collect matrix values dynamically based on the matrix size
            for i in range(1, matrix_size + 1):
                for j in range(1, matrix_size + 1):
                    # Dynamically get the values from the POST data using the correct field name
                    field_name = f'matrix_{i}_{j}'
                    value = request.POST.get(field_name)
                    print(f"row: {i}")
                    print(f"col: {j}")
                    matrix_values[i-1][j-1] = value

            # Now you can process the matrix_values as needed
            print(matrix_values)  
            # Calculate eigenvalues and eigenvectors
            eigenvalues, eigenvectors = np.linalg.eig(matrix_values)
            print(eigenvalues)
            print(eigenvectors)
            eigenvalues = np.round(eigenvalues, decimals=2)
            eigenvectors = np.round(eigenvectors, decimals=2)
            
            row_range = list(range(1, matrix_size + 1))
            return render(request, 'matrix_output.html', {
                'matrix_size': matrix_size,
                'matrix_values': matrix_values.tolist(),
                'row_range': row_range,
                'col_range': row_range,
                'eigenvalues':eigenvalues.tolist(),
                'eigenvectors':eigenvectors.tolist()
            })
    else:
        form = MatrixForm()

    return render(request, 'matrix_form.html', {'form': form})