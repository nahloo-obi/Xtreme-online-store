from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget





class CheckoutForm(forms.Form):
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(
        attrs={
            'class': 'custom-select d-block w 100'
        }
    ))    

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()