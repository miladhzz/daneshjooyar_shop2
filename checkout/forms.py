from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    mobile = forms.CharField(max_length=11)
    address = forms.CharField(max_length=500)
    postal_code = forms.CharField(max_length=10)
    city = forms.IntegerField()


class AddToCartForm(forms.Form):
    product_id = forms.CharField()
    quantity = forms.IntegerField()
    update = forms.IntegerField()
