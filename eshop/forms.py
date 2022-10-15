from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from eshop.models import Product, HelpdeskContact
from django.contrib.auth.forms import UserCreationForm

class ProductReviewForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    score = forms.IntegerField(min_value=0, max_value=5)
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    text = forms.CharField(widget=forms.Textarea)

class HeldeskContactForm(forms.ModelForm):
    class Meta:
        model = HelpdeskContact
        fields = ("email", "nazev", "text")

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
