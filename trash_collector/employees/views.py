from django.db.models.fields import DateField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Employee
from datetime import date
import calendar


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        Customer = apps.get_model('customers.Customer')
        curr_date = date.today()
        day_of_week = calendar.day_name[curr_date.weekday()]
        todays_customers = Customer.objects.filter(weekly_pickup = day_of_week, )
        context = {
            'logged_in_employee':logged_in_employee,
            'curr_date': curr_date,
            'day_of_week': day_of_week,
            'todays_customers': todays_customers,
        }
        
        return render(request, 'employees/index.html',context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        route_from_form = request.POST.get('route_zip')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form, route_zip=route_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')
    
