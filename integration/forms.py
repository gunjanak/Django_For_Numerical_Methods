from django import forms

# class TrapezoidalForm(forms.Form):
#     formula = forms.CharField(label='Formula',max_length=100)
#     lower_limit = forms.FloatField(label='Lower Limit')
#     upper_limit = forms.FloatField(label='Upper Limit')
#     steps = forms.IntegerField(label='Steps')
    

from django import forms

class IntegrationForm(forms.Form):
    formula = forms.CharField(label='Formula', max_length=100)
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps', required=False)
    integration_method = forms.ChoiceField(
        label='Integration Method',
        choices=[
            ('gauss_two_point', 'Gauss Quadrature (Two Points)'),
            ('gauss_three_point', 'Gauss Quadrature (Three Points)'),
            ('trapezoidal', 'Trapezoidal Method'),
            ('simpson_one', 'Simpson\'s 1/3'),
            ('simpson_three', 'Simpson\'s 3/8'),
            ('Romberg_integration','Romberg Integration'),
            # Add more options as needed
        ],
        initial='gauss_two_point',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['steps'].required = False

    def clean(self):
        cleaned_data = super().clean()
        integration_method = cleaned_data.get('integration_method')
        steps = cleaned_data.get('steps')

        # Additional validation based on integration method
        if integration_method == 'trapezoidal' and (steps is None or steps <= 0):
            self.add_error('steps', 'For Trapezoidal Method, the steps value must be greater than zero.')

        if integration_method == 'simpson_one' and (steps is None or steps <= 0 or steps % 2 != 0):
            self.add_error('steps', 'For Simpson\'s 1/3, the steps value must be greater than zero and an even number.')

        if integration_method == 'simpson_three' and (steps is None or steps <= 0 or steps % 3 != 0):
            self.add_error('steps', 'For Simpson\'s 3/8, the steps value must be greater than zero and a multiple of three.')

        return cleaned_data


# class SimpsonOneForm(forms.Form):
#     formula = forms.CharField(label='Formula',max_length=100)
#     lower_limit = forms.FloatField(label='Lower Limit')
#     upper_limit = forms.FloatField(label='Upper Limit')
#     steps = forms.IntegerField(label='Steps')

#     def clean_steps(self):
#         steps = self.cleaned_data.get('steps')

#         if steps is not None and steps % 2 != 0:
#             raise forms.ValidationError("Number of steps must be an even number.")

#         return steps
    

# class SimpsonThreeForm(forms.Form):
#     formula = forms.CharField(label='Formula',max_length=100)
#     lower_limit = forms.FloatField(label='Lower Limit')
#     upper_limit = forms.FloatField(label='Upper Limit')
#     steps = forms.IntegerField(label='Steps')

#     def clean_steps(self):
#         steps = self.cleaned_data.get('steps')

#         if steps is not None and steps % 3 != 0:
#             raise forms.ValidationError("Number of steps must be multiple of three.")

#         return steps