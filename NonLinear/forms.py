from django import forms

class NonlinearEquationForm(forms.Form):
    formula = forms.CharField(label='Formula', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    integration_method = forms.ChoiceField(
        label='Method',
        choices=[
            ('bisection', 'Bisection'),
            ('newton_raphson', 'Newton Raphson'),
            ('secant', 'Secant'),
            ('false_position', 'False Position'),
            ('fixed_point', 'Fixed Point')
        ],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'method-selector'})
    )
    x0 = forms.FloatField(label='X0', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'x0'}))
    xn = forms.FloatField(label='Xn', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'xn'}))
    error = forms.FloatField(label='Error', widget=forms.NumberInput(attrs={'class': 'form-control'}))

