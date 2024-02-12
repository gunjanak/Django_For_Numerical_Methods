from django import forms

class TrapezoidalForm(forms.Form):
    formula = forms.CharField(label='Formula',max_length=100)
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')
    
from django import forms

class IntegrationForm(forms.Form):
    formula = forms.CharField(label='Formula', max_length=100)
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')
    integration_method = forms.ChoiceField(
        label='Integration Method',
        choices=[
            ('gauss_two_point', 'Gauss Quadrature (Two Points)'),
            ('gauss_three_point', 'Gauss Quadrature (Three Points)'),
            ('trapezoidal', 'Trapezoidal Method'),
            # Add more options as needed
        ],
        initial='gauss_two_point',  # Set the initial value
        widget=forms.Select(attrs={'class': 'form-control'})  # Add CSS class for styling
    )


class SimpsonOneForm(forms.Form):
    formula = forms.CharField(label='Formula',max_length=100)
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')

    def clean_steps(self):
        steps = self.cleaned_data.get('steps')

        if steps is not None and steps % 2 != 0:
            raise forms.ValidationError("Number of steps must be an even number.")

        return steps
    

class SimpsonThreeForm(forms.Form):
    formula = forms.CharField(label='Formula',max_length=100)
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')

    def clean_steps(self):
        steps = self.cleaned_data.get('steps')

        if steps is not None and steps % 3 != 0:
            raise forms.ValidationError("Number of steps must be multiple of three.")

        return steps