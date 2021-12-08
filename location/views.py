#from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import json
#from django.db import transaction
#from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from datetime import date 
#from django.db.models import Q
from django.utils import timezone
from django.template import RequestContext
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
#@login_required(login_url='manage_login')
def country_grid(request):
    return render(request,'shravanmanagemet/shravancare_country_grid.html')


#@login_required(login_url='manage_login')
def state_grid(request):
    return render(request,'shravanmanagemet/shravancare_state_grid.html')

#@login_required(login_url='manage_login')
def city_grid(request):
    return render(request,'shravanmanagemet/shravancare_city_grid.html')

#@login_required(login_url='manage_login')
def pincode_grid(request):
    return render(request,'shravanmanagemet/shravancare_pincode_grid.html')    