from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/<int:year>', views.calendar, name='calendar'),
    path('calendar/<int:year>/<int:month>', views.calendar, name='calendar'),
    ]