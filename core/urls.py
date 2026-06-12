from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.views.generic import RedirectView


urlpatterns =  [


     path("login/", views.login_view, name="login"),
    
    
     path('', views.home),


    path('home/', RedirectView.as_view(url='/login/'), name='home'),

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
        
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),

        path('upcoming-bookings/', views.upcoming_bookings),

path('completed-moves/', views.completed_moves),
path('business-rule/', views.business_rule),
path(
    'monthly-expense/',
    views.add_monthly_expense
),

path(
    'daily-expense-report/',
    views.daily_expense_report,
    name='daily_expense_report'
),

path(
    'monthly-expense-report/',
    views.monthly_expense_report,
    name='monthly_expense_report'
),



path("profit-loss/", views.profit_loss, name="profit_loss"),

path(
    'profit-details/<int:month>/',
    views.profit_details
),



path('admin-dashboard/', views.admin_dashboard),

path('employee-dashboard/', views.dashboard),

path(
    'employee-monthly-expense/',
    views.employee_monthly_expense
),

path(
    'employee-daily-expense/',
    views.employee_daily_expense
),

path(
    'employee-business-rule/',
    views.employee_business_rule,
),

path(
    'total-progress/',
    views.total_progress,
),

path("fix-user/", views.fix_user),
   
 ]