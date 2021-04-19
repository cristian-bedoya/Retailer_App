"""retailer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from api import views
from django.contrib import admin
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/signup', views.UserRegistrationView.as_view()),
    url(r'^api/login', views.UserLoginView.as_view()),
    url(r'^api/profile', views.UserProfileView.as_view()),
    url(r'^api/users/$', views.users_list),
    url(r'^api/users/(?P<pk>[0-9]+)$', views.users_detail),
    url(r'^api/orders/$', views.orders_list),
    path('api/orders/<pk>/', views.orders_detail),
    url(r'^api/shippings/$', views.shippings_list),
    url(r'^api/shippings/(?P<pk>[0-9]+)$', views.shippings_detail),
    url(r'^api/payments/$', views.payments_list),
    url(r'^api/payments/(?P<pk>[0-9]+)$', views.payments_detail),
]
