from django import forms

class IntegrationForm(forms.Form):
    formula = forms.CharField(label='Formula',max_length=100)
    lower_limit = forms.FloatField(label='Lower Limit')
    upper_limit = forms.FloatField(label='Upper Limit')
    steps = forms.IntegerField(label='Steps')
    
class FormulaEvaluationForm(forms.Form):
    formula = forms.CharField(label='Formula',max_length=100)
    x_value = forms.FloatField(label='Value of x')

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