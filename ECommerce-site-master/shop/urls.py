from django.urls import path
from .import views
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns=[
    path('',views.index,name='ShopHome'),
    path('about/',views.about,name='Aboutus'),
    path('contact/',views.contact,name='ContactUs'),
    path('tracker/',views.tracker,name="Trackingstatus"),
    path('search/',views.search,name="Search"),
    path('products/<int:id>',views.prodView,name='ProductView'),
    path('checkout/',views.checkout,name="Checkout"),
    path("handlerequest/",views.handlerequest,name="handlerequest"),
    path("login/",views.handlelogin,name='handlelogin'),
    path("signup/",views.handlesignup,name="handlesignup"),
    path("logout/",views.handlelogout,name="handlelogout"),
]