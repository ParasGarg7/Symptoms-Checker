from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('diagnosis',views.diagnosis, name='diagnosis'),
    path('issue',views.issue, name='issue'),
]