from django.urls import path,include
from . import views
from django.conf.urls.i18n import i18n_patterns
from .models import Factor

'''

---This is for activate djangoRestFramework---

from rest_framework import routers, serializers, viewsets


class User1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User1
        fields = ['name', 'personeli', 'etebar', 'pic', 'number']


class User1ViewSet(viewsets.ModelViewSet):
    queryset = User1.objects.all()
    serializer_class = User1Serializer


router = routers.DefaultRouter()
router.register(r'personel', User1ViewSet)

---and add this line to below urlpatterns---

path('api', include(router.urls)),

'''

urlpatterns = [
        path('', views.index),
        path('changepass/', views.changepass),
        path('makefactor/', views.makefactor),
	path('printfactor/', views.printfactor),
	path('printfactorbarcode/', views.printfactorbarcode),
	path('factorlist/', views.factorlist),
	path('editfactor/', views.editfactor),
	path('delfactor/', views.delfactor),
        path('delobj/', views.delobj),
        path('addcustomer/', views.addcustomer),
        path('addseller/', views.addseller),
        path('addproduct/', views.addproduct),
	path('signin/', views.signin),
	path('logout/', views.logout_form),
	path('uploadtpl/', views.uploadtpl),     
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

