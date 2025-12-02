from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,FileResponse,JsonResponse,Http404
from django.db.models import Avg, Count, Min, Sum
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import os,random,json,base64
from .forms import Factor_form, Productlst_form
from .models import Factor, Productlst
from docxtpl import DocxTemplate
from docxtpl import InlineImage
import platform, random
from docx.shared import Mm
from pathlib import Path
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape
from django.contrib.staticfiles import finders
from django.conf import settings
import pyqrcode
if platform.system() == "Windows":
	from docx2pdf import convert
####################################################################
def index(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:		
		return render(request, 'efactor/ou.html')
	except:
		raise Http404("Not Found")
####################################################################
def logout_form(request):
	try:
		logout(request)
	except:
		pass
	return redirect ('/')
####################################################################
def signin(request):
    try:
        if request.method == 'POST':
            #otp_chk=pyotp.TOTP('H4ZT2CIHQM5XO2VUSZPHWTBHMNQBDY3B')
            username=request.POST['username']
            password=request.POST['password']
            #if username=='admin':
            #    if otpcode!=otp_chk.now():
            #        return redirect ('/')
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request , user)
                return redirect ('/')
            else:
                return render(request, 'efactor/login.html')
    except:
        return render(request, 'efactor/login.html')
    return render(request, 'efactor/login.html')
####################################################################
def changepass(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:
		if request.method == 'POST':
				form = PasswordChangeForm(request.user, request.POST)
				if form.is_valid():
					#instance=form.save(commit=False)
					#instance.pic.name="images/{}.png".format(instance.id)
					#instance.save()
					form.save()
					update_session_auth_hash(request, form.user)
					return render(request, 'erscipcard/ou.html', {'memo':'گذرواژه شما با موفقیت تغییر یافت', 'var1' : 1 })
				else:
					return render(request, 'erscipcard/ou.html', {'memo':'خطا در تغییر گذرواژه', 'var1': 1 })
		else:
					form = PasswordChangeForm(request.user)
					return render(request, 'erscipcard/ou.html', {'form': form ,  'dest' : 'changepass' ,'idx' : 1 , 'var1' : 2  })
	except:
		pass
	return redirect("/")
####################################################################
def makefactor(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:
		if request.method == 'POST':
			idx = request.POST['factor_id']
			ins1=Factor.objects.get(id = idx)
			form = Factor_form(request.POST, instance = ins1)
			form2 = Productlst_form(request.POST)
			if form.is_valid():
				form.save()
			if form2.is_valid():
				form2.save()
			factor = Factor.objects.get(id = idx)
			obj = Productlst.objects.filter(factor_id=factor)
			return render(request, 'efactor/ou.html', {'form': form , 'form2' : form2 ,   'dest' : 'makefactor' , 'factor' : factor , 'obj' : obj , 'idx' : factor.id , 'var1' : 4  })		
		else:
			factor = Factor()
			factor.save()
			factor = Factor.objects.last()
			form = Factor_form(instance = factor)
			form2 = Productlst_form(initial={'factor_id' : factor})
			obj = Productlst.objects.filter(factor_id=factor)
			return render(request, 'efactor/ou.html', {'form': form , 'form2' : form2 ,   'dest' : 'makefactor' , 'factor' : factor , 'obj' : obj , 'idx' : factor.id , 'var1' : 4  })
	except:
		pass
	return redirect("/")
####################################################################
def printfactor(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:                
		doc=DocxTemplate("1.docx") if os.path.isfile("1.docx") else DocxTemplate(finders.find("1.docx"))
		if request.method == 'GET':        
				idx = request.GET['id']
				title = request.GET['title']
				factor_data=Factor.objects.get(id = idx)
				product=Productlst.objects.filter(factor_id = idx)
		price = 0
		for u in product:
				price += int(u.obj_name.fee) * int(u.number)
		context = {"data" : factor_data , "factor" : product , "sum" : price , "title" : title}
		doc.render(context)
		doc.save("aa.docx")
		del doc
		if platform.system() == "Windows":
				os.system("docx2pdf {}".format('aa.docx'))
		if platform.system() == "Linux":
				os.system("sudo lowriter --convert-to pdf  {}".format("aa.docx"))
		f = open("aa.pdf", 'rb')
		pdf_contents = f.read()
		f.close()
		response = HttpResponse(pdf_contents, content_type='application/pdf')
		return response
	except:
		pass
	return redirect("/")
####################################################################
def printfactorbarcode(request):
	if not request.user.is_authenticated:
		return render (request,'erscipcard/login.html' )
	try:
		doc=DocxTemplate("1.docx") if os.path.isfile("1.docx") else DocxTemplate(finders.find("1.docx"))
		if request.method == 'GET': 
			barcode = request.GET['q']
			title = request.GET.get('title', 'فاکتور کالا و خدمات')		
			factor=Factor.objects.get(barcode = barcode)
			product=Productlst.objects.filter(factor_id = factor)
		price = 0
		for u in product:
				price += int(u.obj_name.fee) * int(u.number)
		context = {"data" : factor_data , "factor" : product , "sum" : price , "title" : title}
		doc.render(context)
		doc.save("aa.docx")
		del doc
		if platform.system() == "Windows":
				os.system("docx2pdf {}".format('aa.docx'))
		if platform.system() == "Linux":
				os.system("sudo lowriter --convert-to pdf  {}".format("aa.docx"))
		f = open("aa.pdf", 'rb')
		pdf_contents = f.read()
		f.close()
		response = HttpResponse(pdf_contents, content_type='application/pdf')
		return response
	except:
		pass
	return redirect("/")
####################################################################
def factorlist(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:
	    if request.method == 'POST':
	        data = request.POST['idnum']
	        objlst=Factor.objects.filter(name__contains = data ).order_by('id')
	        return render(request, 'efactor/ou.html', {'data': data , 'objlst' : objlst , 'var1' : 3 })
	    else:
	        data = ""
	        objlst=Factor.objects.all().order_by('id')
	        return render(request, 'efactor/ou.html', {'data': data , 'objlst' : objlst , 'var1' : 3 })
	except:
		pass
	return redirect("/")
####################################################################
def editfactor(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:
		idx = request.GET['id']			
		factor = Factor.objects.get(id = idx)
		form = Factor_form(instance = factor)
		form2 = Productlst_form(initial={'factor_id' : factor})
		obj = Productlst.objects.filter(factor_id=factor)
		return render(request, 'efactor/ou.html', {'form': form , 'form2' : form2 ,   'dest' : 'makefactor' , 'factor' : factor , 'obj' : obj , 'idx' : factor.id , 'var1' : 4  })	
	except:
	    return redirect("/")
	return redirect("/")
####################################################################
def delfactor(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:
		if request.method == 'GET':
			idx = request.GET['id']
			Factor.objects.get(id = idx).delete()
	except:
		pass
	return redirect("/factorlist")
####################################################################
def delobj(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html' )
	try:
		if request.method == 'GET':
			idx = request.GET['id']
			obj = Productlst.objects.get(id = idx)			
			Productlst.objects.get(id = idx).delete()
			factor = Factor.objects.get(id = obj.factor_id.id)
			form = Factor_form(instance = factor)
			form2 = Productlst_form(initial={'factor_id' : factor})
			obj = Productlst.objects.filter(factor_id=factor)
			return render(request, 'efactor/ou.html', {'form': form , 'form2' : form2 ,   'dest' : 'makefactor' , 'factor' : factor , 'obj' : obj , 'idx' : factor.id , 'var1' : 4  })	
	except:
		pass
	return redirect("/")
####################################################################
def uploadtpl(request):
	if not request.user.is_authenticated:
		return render (request,'efactor/login.html')
	try:
		if request.method == 'POST':
			f=request.FILES['file']
			with open("1.docx", 'wb') as destination:
				for chunk in f.chunks():
				    destination.write(chunk)
			return render(request, 'efactor/ou.html',{'memo' : 'فایل آپلود شد!' , 'var1' : 1 })
		else:
			return render(request, 'efactor/ou.html', {'var1' : 7 })
	except:
		pass
	return render(request, 'efactor/ou.html', {'memo': 'خطا در سرور' , 'var1' : 1 })
####################################################################
