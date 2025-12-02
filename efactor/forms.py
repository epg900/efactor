from django import forms
from .models import Factor,Product,Productlst,Seller,Customer
from .widget import JalaliDateWidget
from django.conf import settings

class Factor_form(forms.ModelForm):
    class Meta:
        model = Factor
        fields = ['seller_name','customer_name','date']
        widgets = { "date": JalaliDateWidget }

class Productlst_form(forms.ModelForm):
    class Meta:
        model = Productlst
        fields = ['obj_name','number','factor_id']
        

        


