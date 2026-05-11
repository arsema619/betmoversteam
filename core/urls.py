from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.dashboard),

    path(
        'add-booking/',
        views.add_booking
    ),

    path(
        'add-expense/',
        views.add_expense
    ),

    path(
        'edit-booking/<int:id>/',
        views.edit_booking
    ),

    path(
        'delete-booking/<int:id>/',
        views.delete_booking
    ),

    path(
        'edit-expense/<int:id>/',
        views.edit_expense
    ),

    path(
        'delete-expense/<int:id>/',
        views.delete_expense
    ),

    path(
        'reports/',
        views.reports
    ),

    path('accounts/', include('django.contrib.auth.urls')),
        
        path('logout/', auth_views.LogoutView.as_view(), name='logout')
   
 ]