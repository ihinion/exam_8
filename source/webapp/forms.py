from django import forms
from django.forms import CheckboxSelectMultiple
from webapp.models import Product, Review


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Search')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['author', 'product']