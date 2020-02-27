from django import forms
from .models import Order

class Signup(forms.Form):
    username=forms.CharField()
    email=forms.CharField()
    postCode=forms.CharField()
    cpass=forms.CharField(min_length=8)
    password=forms.CharField(min_length=8)


class Login(forms.Form):
    email=forms.CharField()
    password=forms.CharField()


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone','email', 'location']


class OrderConfirmation(forms.Form):
    order_id = forms.IntegerField()


