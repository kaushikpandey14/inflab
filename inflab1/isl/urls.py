from django.conf.urls import url
from django.urls import path
from isl import views
from django.contrib import admin

app_name = 'isl'

urlpatterns = [
    path('',views.general,name='base'),
    path('general1',views.general1,name='general1')

]