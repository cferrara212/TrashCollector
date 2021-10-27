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
        days_customers = Customer.objects.filter(weekly_pickup = day_of_week)
        customers_on_route = days_customers.filter(zip_code = logged_in_employee.route_zip)
        customers_not_suspended = customers_on_route.exclude(suspend_start__lt = curr_date, suspend_end__gt = curr_date)
        customers_to_pickup = customers_not_suspended.exclude(date_of_last_pickup = curr_date)
        one_time_pickup = Customer.objects.filter(one_time_pickup = curr_date)
        one_time_in_route = one_time_pickup.filter(zip_code = logged_in_employee.route_zip)
        one_time_pickup_final = one_time_in_route.exclude(date_of_last_pickup = curr_date)
        
        
        context = {
            'logged_in_employee':logged_in_employee,
            'curr_date': curr_date,
            'day_of_week': day_of_week,
            'customers_to_pickup': customers_to_pickup,
            'one_time_pickup_final': one_time_pickup_final,
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
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        route_from_form = request.POST.get('route_zip')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.route_zip = route_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def schedule(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        day_from_form = request.POST.get('day')
        Customer = apps.get_model('customers.Customer')
        days_customers = Customer.objects.filter(weekly_pickup = day_from_form)
        days_customers_final = days_customers.filter(zip_code = logged_in_employee.route_zip)
        context = {
            'day_from_form': day_from_form,
            'days_customers_final': days_customers_final
        }
        return render(request, 'employees/schedule_details.html', context)
     
    else:
        return render(request, 'employees/schedule.html')


@login_required
def schedule_details(request):
    
    return render(request, 'employees/schedule_details.html')


@login_required
def confirm(request,customer_id):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    curr_date = date.today()
    Customer = apps.get_model('customers.Customer')
    this_customer = Customer.objects.get(pk = customer_id)
    this_customer.date_of_last_pickup=curr_date
    this_customer.balance += 20
    this_customer.save()
    context = {
        'logged_in_employee': logged_in_employee
    }
   
    return HttpResponseRedirect(reverse('employees:index'))

    
