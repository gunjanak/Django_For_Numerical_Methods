from django.shortcuts import render
from django import forms

class MatrixForm(forms.Form):
    MATRIX_CHOICES = [(2, '2x2'), (3, '3x3'),(4, '4x4')]

    matrix_size = forms.ChoiceField(choices=MATRIX_CHOICES, label="Choose Matrix Size")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.matrix_size = self.initial.get('matrix_size', None)




class LinearSystemForm(forms.Form):
    EQUATION_CHOICES = [(2, '2 Equations (2 Variables)'), 
                        (3, '3 Equations (3 Variables)'), 
                        (4, '4 Equations (4 Variables)')]

    no_of_equations = forms.ChoiceField(choices=EQUATION_CHOICES, label="Number of Equations/Variables")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.no_of_equations = self.initial.get('no_of_equations', None)
        
        
   