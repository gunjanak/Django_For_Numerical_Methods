from django import forms

class InterpolationForm(forms.Form):
    POINT_CHOICES = [(i, f'{i} Points') for i in range(2, 11)]  # Allow 2 to 10 points
    ALGORITHM_CHOICES = [
        ('lagrange', 'Lagrange'),
        ('cdd', 'Central Divided Differences (CDD)'),
        ('fdd', 'Forward Divided Differences (FDD)'),
        ('bdd', 'Backward Divided Differences (BDD)'),
        ('cubic_spline', 'Cubic Spline Interpolation'),
        ('linear', 'Linear Interpolation'),
        ('polynomial', 'Polynomial Interpolation'),
    ]

    num_points = forms.ChoiceField(choices=POINT_CHOICES, label="Number of Points")
    algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES, label="Interpolation Algorithm")
    x_in = forms.FloatField(label="Value of x_in", required=True, help_text="Enter the x value to interpolate.")
