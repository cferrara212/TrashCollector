from django.db.models.fields import DateField
from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from datetime import date
import calendar

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    curr_date = date.today()
    day_of_week = calendar.day_name[curr_date.weekday()]
    todays_customers = Customer.objects.filter(weekly_pickup = day_of_week)
    context = {
        'curr_date': curr_date,
        'day_of_week': day_of_week,
        'todays_customers': todays_customers,
    }
    
    return render(request, 'employees/index.html',context)
    
