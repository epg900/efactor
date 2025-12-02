from django.contrib import admin
from .models import Factor,Product,Productlst,Seller,Customer
# Register your models here.

admin.site.register(Product)
admin.site.register(Productlst)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Factor)
