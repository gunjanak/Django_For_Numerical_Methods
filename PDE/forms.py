from django import forms

class LaplaceForm(forms.Form):
    
    top = forms.FloatField(label="Value of Top", required=True)
    left = forms.FloatField(label="Value of Left", required=True)
    right = forms.FloatField(label="Value of Right", required=True)
    bottom = forms.FloatField(label="Bottom", required=True)
    
    
class PoissonForm(forms.Form):
    formula = forms.CharField(
        label="Formula",
        widget=forms.TextInput(attrs={'placeholder': 'Enter a formula'}),
        required=True
    )
    f1_x = forms.FloatField(label="X value of f1", required=True)
    f1_y = forms.FloatField(label="Y value of f1", required=True)
    f2_x = forms.FloatField(label="X value of f2", required=True)
    f2_y = forms.FloatField(label="Y value of f2", required=True)
    f3_x = forms.FloatField(label="X value of f3", required=True)
    f3_y = forms.FloatField(label="Y value of f3", required=True)
    f4_x = forms.FloatField(label="X value of f4", required=True)
    f4_y = forms.FloatField(label="Y value of f4", required=True)
    
    