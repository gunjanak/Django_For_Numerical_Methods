from django.shortcuts import render
from django import forms

class MatrixForm(forms.Form):
    MATRIX_CHOICES = [(2, '2x2'), (3, '3x3'),(4, '4x4')]

    matrix_size = forms.ChoiceField(choices=MATRIX_CHOICES, label="Choose Matrix Size")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.matrix_size = self.initial.get('matrix_size', None)
