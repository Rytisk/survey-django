from django import forms

class IndexForm(forms.Form):
    answer = forms.CharField()