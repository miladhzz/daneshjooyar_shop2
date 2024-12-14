from django import forms


class AddToCartForm(forms.Form):
    product_id = forms.CharField()
    quantity = forms.IntegerField()
    update = forms.IntegerField()
