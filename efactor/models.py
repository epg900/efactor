from django.db import models
from django.core.exceptions import ValidationError
import random

def valid_date(value):
    val=value.split("/")
    if len(val)==3:
        if int(val[0]) in range(1300,1500):
            if int(val[1]) in range(1,7) and int(val[2]) in range(1,32):
                return value
            if int(val[1]) in range(7,13) and int(val[2]) in range(1,31):
                return value
    raise ValidationError("فرمت تاریخ درست نیست!")

def random_string():
    return str(random.randint(10000000000000, 99999999999999))

class Product(models.Model):
    name = models.CharField(max_length=10000 ,verbose_name='نام کالا')
    fee = models.BigIntegerField(verbose_name='في')
    def __str__(self):
        return self.name

class Seller(models.Model):
    name = models.CharField(max_length=100 ,verbose_name='نام و نام خانوادگی')
    tel = models.CharField(max_length=10,null=True,blank=True,verbose_name='شماره تلفن')
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100 ,verbose_name='نام و نام خانوادگی')
    tel = models.CharField(max_length=10,null=True,blank=True,verbose_name='شماره تلفن')
    address = models.CharField(max_length=100,null=True,blank=True,verbose_name='آدرس')
    def __str__(self):
        return self.name

class Factor(models.Model):        
    seller_name = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None, blank=True, null=True,verbose_name='نام فروشنده')
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None, blank=True, null=True,verbose_name='نام خريدار')
    date = models.CharField(max_length=100 ,default=None, blank=True, null=True,validators=[valid_date] ,verbose_name='تاريخ فاکتور')
    barcode = models.CharField(default = random_string, unique = True, max_length=100, verbose_name='بارکد')
    def __str__(self):
        return self.barcode

class Productlst(models.Model):    
    obj_name = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='نام کالا')
    factor_id = models.ForeignKey(Factor, on_delete=models.CASCADE,verbose_name='شماره فاکتور')
    number = models.IntegerField(verbose_name='تعداد')
    def mul(self):
        return self.obj_name.fee * self.number    
    def __str__(self):
	    return self.factor_name.barcode



                    

