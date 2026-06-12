from django.contrib import admin
from .models import *
from .models import BusinessRule

admin.site.register(Profile)
admin.site.register(Booking)
admin.site.register(Expense)
admin.site.register(MonthlyExpense)
admin.site.register(BusinessRule)