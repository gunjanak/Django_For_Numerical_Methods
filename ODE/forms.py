from django import forms

# Define the form
class FormulaInputForm(forms.Form):
    formula = forms.CharField(
        label="Formula",
        widget=forms.TextInput(attrs={'placeholder': 'Enter a formula like 3*x**2+1 or 2*y/x'}),
        required=True
    )
    initial_x = forms.FloatField(label="Initial Value of x", required=True)
    initial_y = forms.FloatField(label="Initial Value of y", required=True)
    height = forms.FloatField(label="Height (h)", required=True)
    final_x = forms.FloatField(label="Final Value of x", required=True)
    method = forms.ChoiceField(
        label="Numerical Method",
        choices=[('Euler', 'Euler'), ('Heun', 'Heun'), ('RK', 'Runge-Kutta')],
        required=True
    )


class SecondOdeForm(forms.Form):
    formula = forms.CharField(
        label="Formula",
        widget=forms.TextInput(attrs={"placeholder": "Enter a formula like y''+y'+6x=5 in form 5-6*x-z"}),
        required=True
    )
    initial_x = forms.FloatField(label="Initial Value of x", required=True)
    initial_y = forms.FloatField(label="Initial Value of y", required=True)
    initial_z = forms.FloatField(label="Initial Value of z", required=True)
    height = forms.FloatField(label="Height (h)", required=True)
    final_x = forms.FloatField(label="Final Value of x", required=True)
    
class SystemOfOdeForm(forms.Form):
    formula_y = forms.CharField(
        label="Formula",
        widget=forms.TextInput(attrs={"placeholder": "Enter a formula like y'=x+y+z in form x+y+z"}),
        required=True
    )
    formula_z = forms.CharField(
        label="Formula",
        widget=forms.TextInput(attrs={"placeholder": "Enter a formula like z'=1+y+z in form 1+y+z"}),
        required=True
    )
    initial_x = forms.FloatField(label="Initial Value of x", required=True)
    initial_y = forms.FloatField(label="Initial Value of y", required=True)
    initial_z = forms.FloatField(label="Initial Value of z", required=True)
    height = forms.FloatField(label="Height (h)", required=True)
    final_x = forms.FloatField(label="Final Value of x", required=True)
    
    