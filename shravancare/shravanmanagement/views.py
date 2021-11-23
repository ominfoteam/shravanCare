from location.models import City, Country, Pincode, State
from django.contrib.auth import login, logout,authenticate
from shravanmanagement.models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from shravanmanagement.forms import *
from django.http import HttpResponse
import json
#from django.db import transaction
#from django.db import IntegrityError, transaction
#from django.forms.formsets import formset_factory
import datetime 
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from django.template import RequestContext, context
from datetime import date ,timedelta

from django.http import JsonResponse
from django.core import serializers
import string
import random
  
# initializing size of string 
#N = 7
#res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N))

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher, make_password
# Create your views here.
def manage_login(request):
    
    if request.method == 'POST':
          username = request.POST['emailid']
          password = request.POST['psw']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  profile=User_Profile.objects.get(user=user.id)
                  login(request,user)
                  request.session["name"] = profile.name
                  
                  # Redirect to index page.
                  
                  return redirect('shravanCareDashboard')
              else:
                  # Return a 'disabled account' error message
                  messages.error(request,"You're account is disabled")
          else:
              # Return an 'invalid login' error message.
              messages.error(request,"invalid login details " + username + " " + password)
              return render(request,'shravanmanagemet/login.html', {})
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request,'shravanmanagemet/login.html')


@login_required(login_url='manage_login')
def shravanCareDashboard(request):
    salesreqs=Customer_Request.objects.filter(reqtype="SALES").exclude(querystatus="CLOSE")
    custreqs=Customer_Request.objects.filter(reqtype="CUSTOMER SUPPORT").exclude(querystatus="CLOSE")
    invoice=InvoiceManagement.objects.exclude(paymentstatus='Paid')
    today = date.today()
    todaysvis=IcareVisitScheduling.objects.filter(visitdate__year=today.year, visitdate__month=today.month, visitdate__day=today.day)
    context={'salesreqs':salesreqs,"custreqs":custreqs,"invoice":invoice,"todaysvis":todaysvis}    
    return render(request,'shravanmanagemet/shravancare_dashboard_frame.html',context)   

@login_required(login_url='manage_login')
def addTaskCategory(request):
    if request.method == 'POST':
        categName = request.POST['taskcatname']
        position = request.POST['taskcatpos']
        categ_description = request.POST['cat-desc']

        # creating Task Categ here
        managetaskcateg = Task_Category.objects.create(categName=categName,position=position, categ_description=categ_description) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        managetaskcateg.save() # saving created Task Categ
        return redirect('gridTaskCategory')
    else:
        
        context={"taskcateg":True}
        return render(request, 'shravanmanagemet/shravancare_task_category_manage.html', context)

@login_required(login_url='manage_login')
def addTask(request):
    if request.method == 'POST':
        taskinstance=Task_Category.objects.get(id=request.POST['task_cat'])
        taskName = request.POST['task_name']
        categ_id = taskinstance
        question = request.POST['ques']
        is_due = request.POST['isdue']
        position = request.POST['position']

        # creating Task here
        managetask = Task.objects.create(taskName=taskName,is_due=is_due, categ_id=categ_id, question=question,position=position) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        managetask.save() # saving created Task
        return redirect('gridTask')
    else:
        taskcat=Task_Category.objects.all()
        context={'taskcat':taskcat}
    return render(request, 'shravanmanagemet/shravancare_task_manage.html', context)


@login_required(login_url='manage_login')
def gridTaskCategory(request):
    
    taskcat=Task_Category.objects.all()
    context={'taskcat':taskcat}
    
    return render(request, 'shravanmanagemet/shravancare_task_category_grid.html', context)

@login_required(login_url='manage_login')
def gridTask(request):
    tasks=Task.objects.all().order_by('position')
    context={'tasks':tasks}
    
    return render(request, 'shravanmanagemet/shravancare_task_grid.html', context)
def logout_backend(request):
    logout(request)
    request.session.flush()
    return redirect('manage_login')

def loadCity(request):
    state_id = request.GET.get('state_id')
    #print(state_id)
    cities = City.objects.filter(state=state_id).all()
    return render(request, 'shravanmanagemet/city_dropdown.html', {'cities': cities})

def loadPincode(request):
    #city_id = request.GET.get('ctiy_id')
    temp = request.GET.get('temp')
    #print(temp)
    pincodes = Pincode.objects.filter(city=temp).all()
    return render(request, 'shravanmanagemet/pincode_dropdown.html', {'pincodes': pincodes})

def loadState(request):
    country_id = request.GET.get('country_id')
    #print(country_id)
    states = State.objects.filter(country=country_id).all()
    return render(request, 'shravanmanagemet/state_dropdown.html', {'states': states})

@login_required(login_url='manage_login')
def viewTaskCategory(request,pk):
    taskcatdetails=Task_Category.objects.get(id=pk)
    context={'taskcatdetails':taskcatdetails,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/shravancare_task_category_manage.html', context)

@login_required(login_url='manage_login')
def editTaskCategory(request,pk):
    taskcatdetails=Task_Category.objects.get(id=pk)
    context={'taskcatdetails':taskcatdetails}
    if request.method == 'POST':
        taskcatdetails.categName = request.POST['taskcatname']
        taskcatdetails.position = request.POST['taskcatpos']
        taskcatdetails.categ_description = request.POST['cat-desc']
        taskcatdetails.save()
        return redirect('gridTaskCategory')
    return render(request, 'shravanmanagemet/shravancare_task_category_manage.html', context)

@login_required(login_url='manage_login')
def deleteTaskCategory(request,pk):
    taskcatdetails=Task_Category.objects.get(id=pk)
    taskcatdetails.delete()
    return redirect('gridTaskCategory')

@login_required(login_url='manage_login')
def deleteTask(request,pk):
    taskdetails=Task.objects.get(id=pk)
    taskdetails.delete()
    return redirect('gridTask')

@login_required(login_url='manage_login')
def viewTask(request,pk):
    taskdetail=Task.objects.get(id=pk)
    taskcat=Task_Category.objects.all()
    context={'taskdetail':taskdetail,'taskcat':taskcat,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/shravancare_task_manage.html', context)

@login_required(login_url='manage_login')
def editTask(request,pk):
    taskdetail=Task.objects.get(id=pk)
    taskcat=Task_Category.objects.all()
    context={'taskdetail':taskdetail,'taskcat':taskcat}
    if request.method == 'POST':
        taskinstance=Task_Category.objects.get(id=request.POST['task_cat'])
        taskdetail.taskName = request.POST['task_name']
        taskdetail.categ_id = taskinstance
        taskdetail.question = request.POST['ques']
        taskdetail.position = request.POST['position']
        taskdetail.is_due = request.POST['isdue']
        taskdetail.save()
        
        
        return redirect('gridTask')
    return render(request, 'shravanmanagemet/shravancare_task_manage.html', context)



@login_required(login_url='manage_login')
def gridSlider(request):
    
    slider=HomePageSlider.objects.all().order_by('position')
    context={'sliders':slider}
    
    return render(request, 'shravanmanagemet/sharavancare_landing_part_grid.html', context)



@login_required(login_url='manage_login')
def addSlider(request):
    if request.method == 'POST':
        
        position = request.POST.get('positionmain', False)
        sliderimagetemp = request.FILES.get('upFile23')
        fs = FileSystemStorage()
        filename = fs.save(sliderimagetemp.name, sliderimagetemp)
        sliderimage = fs.url(filename) 
        imagetext = request.POST.get('landing-text', False)
        createcslider = HomePageSlider.objects.create(position=position, sliderimage=sliderimage,imagetext=imagetext) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        createcslider.save() # saving created Task Categ
        return redirect('gridSlider')
    else:
                
        context={'addwalah':True}
        return render(request, 'shravanmanagemet/sharavancare_landing_part_manage.html', context)


@login_required(login_url='manage_login')
def editSlider(request,pk):
    slider=HomePageSlider.objects.get(id=pk)
    
    context={'slider':slider}
    if request.method == 'POST':
        
        slider.position = request.POST.get('positionmain', False)
        
        sliderimagetemp = request.FILES.get('upFile23')
        fs = FileSystemStorage()
        filename = fs.save(sliderimagetemp.name, sliderimagetemp)
        slider.sliderimage = fs.url(filename) 
        slider.imagetext = request.POST.get('landing-text', False)
        slider.save()
        
        
        return redirect('gridSlider')
    return render(request, 'shravanmanagemet/sharavancare_landing_part_manage.html', context)

@login_required(login_url='manage_login')
def viewSlider(request,pk):
    slider=HomePageSlider.objects.get(id=pk)
    
    context={'slider':slider,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/sharavancare_landing_part_manage.html', context)




@login_required(login_url='manage_login')
def deleteSlider(request,pk):
    sliderdetails=HomePageSlider.objects.get(id=pk)
    sliderdetails.delete()
    return redirect('gridSlider')



@login_required(login_url='manage_login')
def gridTestimonial(request):
    
    testim=Testimonials.objects.all().order_by('position')
    context={'testim':testim}
    
    return render(request, 'shravanmanagemet/sharavancare_testimonial_grid.html', context)



@login_required(login_url='manage_login')
def addTestimonial(request):
    if request.method == 'POST':
        subtext = request.POST['testimonial_subtext']
        content = request.POST['testimonial_content']
        written_by = request.POST['testimonial_name']
        position = request.POST['testimonial_position']    
        # creating Task Categ here
        createtestim = Testimonials.objects.create(position=position, written_by=written_by, content=content,subtext=subtext) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        createtestim.save() 
        return redirect('gridTestimonial')
    else:
        
        context={}
        return render(request, 'shravanmanagemet/sharavancare_testimonial_manage.html', context)


@login_required(login_url='manage_login')
def editTestimonial(request,pk):
    testim=Testimonials.objects.get(id=pk)
    
    context={'testim':testim}
    if request.method == 'POST':
        
        testim.subtext = request.POST['testimonial_subtext']
        testim.content = request.POST['testimonial_content']
        testim.written_by = request.POST['testimonial_name']
        testim.position = request.POST['testimonial_position']
        testim.save()
        
        
        return redirect('gridTestimonial')
    return render(request, 'shravanmanagemet/sharavancare_testimonial_manage.html', context)

@login_required(login_url='manage_login')
def viewTestimonial(request,pk):
    testim=Testimonials.objects.get(id=pk)
    
    context={'testim':testim,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/sharavancare_testimonial_manage.html', context)

@login_required(login_url='manage_login')
def deleteTestimonial(request,pk):
    testimdetails=Testimonials.objects.get(id=pk)
    testimdetails.delete()
    return redirect('gridTestimonial')


@login_required(login_url='manage_login')
def addEmployee(request):
    
    if request.method == 'POST':
        countryinst=Country.objects.get(id=request.POST['country'])
        stateinst=State.objects.get(id=request.POST['state'])
        cityinst=City.objects.get(id=request.POST['city'])
        pincodeinst=Pincode.objects.get(id=request.POST['city'])
        countemp=CustomUser.objects.exclude(is_customer="True").order_by('-id').first()
        
        username='SC00'+str(countemp.id+1)
        if request.POST['desig'] == 'MANAGEMENT':
            empcreate = CustomUser.objects.create(is_management=True,username=username,email=request.POST['emailid'],is_staff=True,is_superuser=True,password=make_password(username),is_active=True) 
            empcreate.save()
            employeeprofile=User_Profile.objects.create(user=empcreate)
            employeeprofile.name= request.POST['ename']
            employeeprofile.dob= request.POST['dob']
            employeeprofile.gender= request.POST['gender']
            employeeprofile.address= request.POST['addr']
            employeeprofile.mobile= request.POST['mob']
            employeeprofile.country= countryinst
            employeeprofile.state= stateinst
            employeeprofile.city= cityinst
            employeeprofile.pincode= pincodeinst
            employeeprofile.save()
            # saving created Task
        else:
            empcreate = CustomUser.objects.create(is_icare=True,username=username,email=request.POST['emailid'],is_staff=True,is_superuser=False,password=make_password(username),is_active=True) 
            empcreate.save()
            employeeprofile=User_Profile.objects.create(user=empcreate)
            employeeprofile.name= request.POST['ename']
            employeeprofile.dob= request.POST['dob']
            employeeprofile.gender= request.POST['gender']
            employeeprofile.address= request.POST['addr']
            employeeprofile.mobile= request.POST['mob']
            employeeprofile.country= countryinst
            employeeprofile.state= stateinst
            employeeprofile.city= cityinst
            employeeprofile.pincode= pincodeinst
            employeeprofile.description= request.POST['desc']
            employeeprofile.save()
            vaccinationdetails=Icare_ID_Proof.objects.create(user_id=empcreate)
            vaccinationdetails.id_name=request.POST.get('idproof-type')
            imagetemp = request.FILES['upFile'] 
            fs = FileSystemStorage()
            filename = fs.save(imagetemp.name, imagetemp)
            vaccinationdetails.imgurl = fs.url(filename)
            vaccinationdetails.created_by=request.user
            vaccinationdetails.updated_by=request.user
            vaccinationdetails.save()
            if request.method == 'POST' and request.FILES.get('upFile1'):
                vaccinationdetails=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails.id_name=request.POST.get('idproof-type1')
                imagetemp = request.FILES.get('upFile1') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails.imgurl = fs.url(filename)
                vaccinationdetails.created_by=request.user
                vaccinationdetails.updated_by=request.user
                vaccinationdetails.save()
            else:
                pass
            if request.method == 'POST' and request.FILES.get('upFile2') :
                vaccinationdetails=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails.id_name=request.POST.get('idproof-type2')
                imagetemp = request.FILES.get('upFile2') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails.imgurl = fs.url(filename)
                vaccinationdetails.created_by=request.user
                vaccinationdetails.updated_by=request.user
                vaccinationdetails.save()
            else:
                pass
            if request.method == 'POST' and request.FILES.get('upFile3'):
                vaccinationdetails1=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails1.id_name='Vaccination Certificate'
                vaccinationdetails1.is_vaccination='YES'
                imagetemp = request.FILES.get('upFile3') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails1.imgurl = fs.url(filename)
                vaccinationdetails1.created_by=request.user
                vaccinationdetails1.updated_by=request.user
                vaccinationdetails1.save()
            else:
                pass
        messagemain="Hello "+str(request.POST['ename'])+", this is your credentials- Username:"+str(username)+" and Password:"+str(username)
        send_mail("Shravancare Credentials",messagemain,settings.EMAIL_HOST_USER,request.POST['emailid'])
        return redirect('gridEmployee')
    else:
        country=Country.objects.all()
        
        context={'country':country}
    return render(request, 'shravanmanagemet/shravancare_emp_manage.html', context)
@login_required(login_url='manage_login')
def viewEmployee(request,pk):
    icaredetail1=[]
    icaredetail2=[]
    icaredetail3=[]
    countrymain=Country.objects.all()
    empdetail=User_Profile.objects.get(user__username=pk)    
    pincode=Pincode.objects.filter(city=empdetail.pincode.city)
    statemain=State.objects.filter(country=empdetail.pincode.city.state.country)
    citymain=City.objects.filter(state=empdetail.pincode.city.state)
    if(empdetail.user.is_icare == 1):
        docrowcount=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').count()
        if(docrowcount == 1):
            icaredetail1=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').first()
        elif(docrowcount == 2):
            icaredetail1=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').first()
            icaredetail2=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO')[1:2].get()
        elif(docrowcount == 3):
            icaredetail1=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').first()
            icaredetail2=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO')[1:2].get()
            icaredetail3=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').last()
        vaccine=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'YES')
        context={'pincode':pincode,'icare1':icaredetail1,'icare2':icaredetail2,'icare3':icaredetail3,'view':'disabled','vaccine':vaccine,'city':citymain,'state':statemain,'country':countrymain,'empdetail':empdetail}
    else:
        context={'pincode':pincode,'view':'disabled','city':citymain,'state':statemain,'country':countrymain,'empdetail':empdetail}
    return render(request, 'shravanmanagemet/shravancare_emp_manage.html', context)

@login_required(login_url='manage_login')
def editEmployee(request,pk):
    icaredetail1=[]
    icaredetail2=[]
    icaredetail3=[]
    countrymain=Country.objects.all()
    empdetail=User_Profile.objects.get(user__username=pk)    
    pincode=Pincode.objects.filter(city=empdetail.pincode.city)
    statemain=State.objects.filter(country=empdetail.pincode.city.state.country)
    citymain=City.objects.filter(state=empdetail.pincode.city.state)
    if(empdetail.user.is_icare == 1):
        docrowcount=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').count()
        if(docrowcount == 1):
            icaredetail1=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').first()
        elif(docrowcount == 2):
            icaredetail1=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').first()
            icaredetail2=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO')[1:2].get()
        elif(docrowcount == 3):
            icaredetail1=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').first()
            icaredetail2=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO')[1:2].get()
            icaredetail3=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'NO').last()
        vaccine=Icare_ID_Proof.objects.filter(user_id__username=pk).filter(is_vaccination = 'YES')
        context={'pincode':pincode,'isicare':True,'icare1':icaredetail1,'icare2':icaredetail2,'icare3':icaredetail3,'vaccine':vaccine,'city':citymain,'state':statemain,'country':countrymain,'empdetail':empdetail}
    else:
        context={'pincode':pincode,'city':citymain,'state':statemain,'country':countrymain,'empdetail':empdetail}
    if request.method == 'POST':
        countryinst=Country.objects.get(id=request.POST['country'])
        stateinst=State.objects.get(id=request.POST['state'])
        cityinst=City.objects.get(id=request.POST['city'])
        pincodeinst=Pincode.objects.get(id=request.POST['city'])
        empcreate = CustomUser.objects.get(id=empdetail.user.id)
        if(request.POST['isactive'] == "No"):
            empcreate.is_active=False
        else:
            empcreate.is_active=True
        empcreate.save()
        if request.POST['desig'] == 'MANAGEMENT':
            employeeprofile=User_Profile.objects.get(user=empcreate)
            employeeprofile.name= request.POST['ename']
            employeeprofile.dob= request.POST['dob']
            employeeprofile.gender= request.POST['gender']
            employeeprofile.address= request.POST['addr']
            employeeprofile.mobile= request.POST['mob']
            employeeprofile.country= countryinst
            employeeprofile.state= stateinst
            employeeprofile.city= cityinst
            employeeprofile.pincode= pincodeinst
            employeeprofile.save()
            # saving created Task
        else:
            
            employeeprofile=User_Profile.objects.get(user=empcreate)
            employeeprofile.name= request.POST['ename']
            employeeprofile.dob= request.POST['dob']
            employeeprofile.gender= request.POST['gender']
            employeeprofile.address= request.POST['addr']
            employeeprofile.mobile= request.POST['mob']
            employeeprofile.country= countryinst
            employeeprofile.state= stateinst
            employeeprofile.city= cityinst
            employeeprofile.pincode= pincodeinst
            employeeprofile.description= request.POST['desc']
            employeeprofile.save()
            vaccinationdetails=Icare_ID_Proof.objects.filter(user_id=empcreate)
            vaccinationdetails.delete()
            if request.method == 'POST' and request.FILES.get('upFile'):
                vaccinationdetails=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails.id_name=request.POST.get('idproof-type')
                imagetemp = request.FILES.get('upFile') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails.imgurl = fs.url(filename)
                vaccinationdetails.created_by=request.user
                vaccinationdetails.updated_by=request.user
                vaccinationdetails.save()
            if request.method == 'POST' and request.FILES.get('upFile1'):
                vaccinationdetails=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails.id_name=request.POST.get('idproof-type1')
                imagetemp = request.FILES.get('upFile1') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails.imgurl = fs.url(filename)
                vaccinationdetails.created_by=request.user
                vaccinationdetails.updated_by=request.user
                vaccinationdetails.save()
            else:
                pass
            if request.method == 'POST' and request.FILES.get('upFile2') :
                vaccinationdetails=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails.id_name=request.POST.get('idproof-type2')
                imagetemp = request.FILES.get('upFile2') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails.imgurl = fs.url(filename)
                vaccinationdetails.created_by=request.user
                vaccinationdetails.updated_by=request.user
                vaccinationdetails.save()
            else:
                pass
            if request.method == 'POST' and request.FILES.get('upFile3'):
                vaccinationdetails1=Icare_ID_Proof.objects.create(user_id=empcreate)
                vaccinationdetails1.id_name='Vaccination Certificate'
                vaccinationdetails1.is_vaccination='YES'
                imagetemp = request.FILES.get('upFile3') 
                fs = FileSystemStorage()
                filename = fs.save(imagetemp.name, imagetemp)
                vaccinationdetails1.imgurl = fs.url(filename)
                vaccinationdetails1.created_by=request.user
                vaccinationdetails1.updated_by=request.user
                vaccinationdetails1.save()
            else:
                pass
        return redirect('gridEmployee')
    
    return render(request, 'shravanmanagemet/shravancare_emp_manage.html', context)




@login_required(login_url='manage_login')
def deleteCountry(request,pk):
    countrydetails=Country.objects.get(id=pk)
    countrydetails.delete()
    return redirect('gridCountry')

@login_required(login_url='manage_login')
def gridEmployee(request):
    emp=User_Profile.objects.exclude(user__is_customer=True)
    context={'emp':emp}
    
    return render(request, 'shravanmanagemet/shravancare_emp_grid.html', context)

@login_required(login_url='manage_login')
def passwordReset(request,pk):
    emptemp=CustomUser.objects.get(username=pk)
    emp=User_Profile.objects.get(user=emptemp)
    emp.password=make_password(emp.user.username)
    emp.save()
    messagemain="Hello "+str(emp.name)+", this is your reset credentials- Username:"+str(emp.user.username)+" and Password:"+str(emp.user.username)
    send_mail("Shravancare Password Reset",messagemain,settings.EMAIL_HOST_USER,emptemp.email)    
    return redirect('gridEmployee')









@login_required(login_url='manage_login')
def gridCountry(request):
    
    country=Country.objects.all()
    context={'country':country}
    
    return render(request, 'shravanmanagemet/shravancare_country_grid.html', context)



@login_required(login_url='manage_login')
def addCountry(request):
    if request.method == 'POST':
        country_name = request.POST['countryname']
        currency = request.POST['country-currency']
           
        # creating Task Categ here
        createCountry = Country.objects.create(country_name=country_name, currency=currency) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        createCountry.save() 
        return redirect('gridCountry')
    else:
        
        context={}
        return render(request, 'shravanmanagemet/shravancare_country_manage.html', context)


@login_required(login_url='manage_login')
def editCountry(request,pk):
    country=Country.objects.get(id=pk)
    
    context={'country':country}
    if request.method == 'POST':
        
        country.country_name = request.POST['countryname']
        country.currency = request.POST['country-currency']
        country.save()
        
        
        return redirect('gridCountry')
    return render(request, 'shravanmanagemet/shravancare_country_manage.html', context)


@login_required(login_url='manage_login')
def viewCountry(request,pk):
    country=Country.objects.get(id=pk)
    
    context={'country':country,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/shravancare_country_manage.html', context)




@login_required(login_url='manage_login')
def gridState(request):
    state=State.objects.all()
    context={'state':state}
    
    return render(request, 'shravanmanagemet/shravancare_state_grid.html', context)

@login_required(login_url='manage_login')
def gridCity(request):
    city=City.objects.all()
    context={'city':city}
    
    return render(request, 'shravanmanagemet/shravancare_city_grid.html', context)



@login_required(login_url='manage_login')
def gridPincode(request):
    pincode=Pincode.objects.all()
    context={'pincode':pincode}
    
    return render(request, 'shravanmanagemet/shravancare_pincode_grid.html', context)


@login_required(login_url='manage_login')
def addPincode(request):
    countrymain=Country.objects.all()
    zonemain=Zone.objects.all()
    
    if request.method == 'POST':
        city = City.objects.get(id=request.POST['city'])
        pincode_no = request.POST['pincode']
        zone = Zone.objects.get(id=request.POST['zoneid'])
           
        # creating Task Categ here
        createPincode = Pincode.objects.create(pincode_no=pincode_no, city=city,zone=zone) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        createPincode.save() 
        return redirect('gridPincode')
    else:
     
        context={'country':countrymain,'zonemain':zonemain}
        return render(request, 'shravanmanagemet/shravancare_pincode_manage.html', context)

@login_required(login_url='manage_login')
def editPincode(request,pk):
    countrymain=Country.objects.all()
    zonemain=Zone.objects.all()
    pincode=Pincode.objects.get(id=pk)
    statemain=State.objects.filter(country=pincode.city.state.country)
    citymain=City.objects.filter(state=pincode.city.state)
    context={'pincodedetail':pincode,'city':citymain,'state':statemain,'country':countrymain,'zonemain':zonemain}
    if request.method == 'POST':
        pincode.pincode_no = request.POST['pincode']
        pincode.city = City.objects.get(id=request.POST['city'])   
        pincode.zone=Zone.objects.get(id=request.POST['zoneid'])     
        pincode.save()        
        return redirect('gridPincode')
    return render(request, 'shravanmanagemet/shravancare_pincode_manage.html', context)

@login_required(login_url='manage_login')
def viewPincode(request,pk):
    countrymain=Country.objects.all()
    zonemain=Zone.objects.all()
    pincode=Pincode.objects.get(id=pk)
    statemain=State.objects.filter(country=pincode.city.state.country)
    citymain=City.objects.filter(state=pincode.city.state)
    context={'pincodedetail':pincode,'city':citymain,'state':statemain,'zonemain':zonemain,'country':countrymain,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/shravancare_pincode_manage.html', context)

@login_required(login_url='manage_login')
def deletePincode(request,pk):
    pincodedetails=Pincode.objects.get(id=pk)
    pincodedetails.delete()
    return redirect('gridpincode')

@login_required(login_url='manage_login')
def addCity(request):
    countrymain=Country.objects.all()
    
    if request.method == 'POST':
        state = State.objects.get(id=request.POST['state'])
        city_name = request.POST['city']
           
        # creating Task Categ here
        createCity = City.objects.create(state=state, city_name=city_name) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        createCity.save() 
        return redirect('gridCity')
    else:
        
        context={'country':countrymain}
        return render(request, 'shravanmanagemet/shravancare_city_manage.html', context)

@login_required(login_url='manage_login')
def editCity(request,pk):
    countrymain=Country.objects.all()
    city=City.objects.get(id=pk)
    statemain=State.objects.filter(country=city.state.country)
    context={'citydetail':city,'state':statemain,'country':countrymain}
    if request.method == 'POST':
        city.state_name = request.POST['city']
        city.state = State.objects.get(id=request.POST['state'])        
        city.save()        
        return redirect('gridCity')
    return render(request, 'shravanmanagemet/shravancare_city_manage.html', context)


@login_required(login_url='manage_login')
def viewCity(request,pk):
    countrymain=Country.objects.all()
    city=City.objects.get(id=pk)
    statemain=State.objects.filter(country=city.state.country)
    context={'citydetail':city,'state':statemain,'country':countrymain,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/shravancare_city_manage.html', context)

@login_required(login_url='manage_login')
def deleteCity(request,pk):
    citydetails=City.objects.get(id=pk)
    citydetails.delete()
    return redirect('gridCity')

@login_required(login_url='manage_login')
def addState(request):
    countrymain=Country.objects.all()
    if request.method == 'POST':
        gst_code = request.POST['gst-code']
        state_name = request.POST['state']
        country = Country.objects.get(id=request.POST['country'])
           
        # creating Task Categ here
        createState = State.objects.create(gst_code=gst_code, state_name=state_name,country=country) #creating user with the help of User(you have to import it. from django.contrib.auth.models import User)
        
        createState.save() 
        return redirect('gridState')
    else:
        
        context={'country':countrymain}
        return render(request, 'shravanmanagemet/shravancare_state_manage.html', context)
    
    
    
    

@login_required(login_url='manage_login')
def editState(request,pk):
    state=State.objects.get(id=pk)
    countrymain=Country.objects.all()
    context={'statedetail':state,'country':countrymain}
    if request.method == 'POST':
        state.state_name = request.POST['state']
        state.country = Country.objects.get(id=request.POST['country'])
        state.gst_code = request.POST['gst-code']
        state.save()
        
        
        return redirect('gridState')
    return render(request, 'shravanmanagemet/shravancare_state_manage.html', context)

@login_required(login_url='manage_login')
def viewState(request,pk):
    state=State.objects.get(id=pk)
    countrymain=Country.objects.all()
    context={'statedetail':state,'country':countrymain,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/shravancare_state_manage.html', context)


@login_required(login_url='manage_login')
def deleteState(request,pk):
    statedetails=State.objects.get(id=pk)
    statedetails.delete()
    return redirect('gridState')

@login_required(login_url='manage_login')
def editCustomer(request,pk):
    customer=User_Profile.objects.get(user__email=pk)
    eldernames=Customer_Parents.objects.filter(user_id__email=pk)
    parentsdets=Elder_Details.objects.get(user_id__email=pk)
    context={'customer':customer,'eldernames':eldernames,'parentsdets':parentsdets}
    if request.method == 'POST':
        parentsdets.description = request.POST['elder_instruction']
        
        parentsdets.save()
        
        
        return redirect('gridCustomer')

    return render(request, 'shravanmanagemet/shravancare_customer_manage.html', context)


@login_required(login_url='manage_login')
def viewCustomer(request,pk):
    customer=User_Profile.objects.get(user__email=pk)
    eldernames=Customer_Parents.objects.filter(user_id__email=pk)
    parentsdets=Elder_Details.objects.get(user_id__email=pk)
    context={'customer':customer,'eldernames':eldernames,'parentsdets':parentsdets,'view':'readonly'}
    

    return render(request, 'shravanmanagemet/shravancare_customer_manage.html', context)


@login_required(login_url='manage_login')
def gridCustomer(request):
    
    customer=User_Profile.objects.exclude(user__is_customer=False)
    eldernames=Customer_Parents.objects.exclude(user_id__is_customer=False)
    parentsdets=Elder_Details.objects.exclude(user_id__is_customer=False)
    context={'customer':customer,'eldernames':eldernames,'parentsdets':parentsdets}
    
    return render(request, 'shravanmanagemet/shravancare_customer_grid.html', context)

#@login_required(login_url='manage_login')
def icarevisit(request,pk):
    visdata=IcareVisitScheduling.objects.get(id=pk)
    userdetail=User_Profile.objects.get(user=CustomUser.objects.get(id= visdata.cust_id.id))
    
    elderdetail=Elder_Details.objects.get(user_id=CustomUser.objects.get(id= visdata.cust_id.id))
    customerparents=Customer_Parents.objects.filter(user_id=CustomUser.objects.get(id= visdata.cust_id.id))
    eldername=''
    delim = ','
    for parents in customerparents:
        eldername+= parents.parent_name  
        if parents.parent_name != customerparents.last().parent_name:
            eldername+=delim
        
    context={"visdata":visdata,"userdetail":userdetail,"eldername":eldername,"elderdetail":elderdetail,"customerparents":customerparents}
    
    return render(request,'shravanmanagemet/shravancare_icare_partner_visit_index.html', context)


#@login_required(login_url='manage_login')
def icaretasks(request,pk):
    visdata=IcareVisitScheduling.objects.get(id=pk)
    categs=Task_Category.objects.all().order_by('position')
    tasks=Task.objects.all().order_by('position')
    
    context={'categs':categs,'tasks':tasks,"visdata":visdata}
    
    return render(request, 'shravanmanagemet/shravancare_icare_partner_visit_addbill.html', context)




@login_required(login_url='manage_login')
def gridSalesRequest(request):
    
    salesreqs=Customer_Request.objects.filter(reqtype="SALES").exclude(querystatus="CLOSE")
    context={'salesreqs':salesreqs}    
    
    
    return render(request, 'shravanmanagemet/sharavancare_sales_request_grid.html', context)


@login_required(login_url='manage_login')
def editSalesRequest(request,pk):
    salesreq=Customer_Request.objects.get(id=pk)
    context={'salesreq':salesreq}
    if request.method == 'POST':
        salesreq.user_description = request.POST['user-comment']
        salesreq.querystatus = request.POST['cust_salesstatus']
        
        salesreq.save()
        
        
        return redirect('gridSalesRequest')
    
    return render(request, 'shravanmanagemet/sharavancare_sales_request_manage.html', context)


@login_required(login_url='manage_login')
def viewSalesRequest(request,pk):
    salesreq=Customer_Request.objects.get(id=pk)
    context={'salesreq':salesreq,'view':'disabled'}
    
    return render(request, 'shravanmanagemet/sharavancare_sales_request_manage.html', context)
    
@login_required(login_url='manage_login')
def gridCustomerRequest(request):
    custreqs=Customer_Request.objects.filter(reqtype="CUSTOMER SUPPORT").exclude(querystatus="CLOSE")
    context={'custreqs':custreqs}    
    
    return render(request, 'shravanmanagemet/sharavancare_customer_support_grid.html', context)
    

@login_required(login_url='manage_login')
def editCustomerRequest(request,pk):
    custreq=Customer_Request.objects.get(id=pk)
    context={'custreq':custreq}
    if request.method == 'POST':
        custreq.user_description = request.POST['user-comment']
        custreq.querystatus = request.POST['cust_salesstatus']
        
        custreq.save()
        
        
        return redirect('gridCustomerRequest')

    
    
    return render(request, 'shravanmanagemet/sharavancare_customer_support_manage.html', context)
  
@login_required(login_url='manage_login')
def viewCustomerRequest(request,pk):
    custreq=Customer_Request.objects.get(id=pk)
    context={'custreq':custreq,'view':'disabled'}
    
    
    return render(request, 'shravanmanagemet/sharavancare_customer_support_manage.html', context)


@login_required(login_url='manage_login')
def addInvoice(request):
    if request.method == 'POST':
        invcount=InvoiceManagement.objects.all().count()
        invdate=date.today()
        
        if invcount > 0:
            invno=InvoiceManagement.objects.last()
            newinvno="SC/INV/"+str(invno.countervalue+1)
        else:
            newinvno="SC/INV/1"
        

        invdata=InvoiceManagement.objects.create(invoiceno=newinvno)
        invdata.countervalue=invcount+1
        invdata.invdate=invdate
        invdata.cust_id=CustomUser.objects.get(id=request.POST['custid']) 
        invdata.custname=request.POST['custname']
        invdata.custaddr=request.POST['cust_address']
        invdata.custcity=City.objects.get(city_name=request.POST['cust-city']) 
        invdata.eldersname=request.POST['elder-name']
        invdata.elderpincode=Pincode.objects.get(id=request.POST['elderpin'])
        invdata.elderaddr=request.POST['elder_address']
        invdata.eldercontact=request.POST['eldercontact']
        invdata.custcontact=request.POST['custmobile']
        invdata.invdescribe=request.POST['invoice-desc']
        invdata.invoicetype=request.POST['invoice-type']
        
        invdata.subtotal=float(request.POST['rate'])
        invdata.gstpercentage=float(18)
        invdata.gstamount=float(request.POST['cgst'])+float(request.POST['sgst'])
        invdata.cgst=float(request.POST['cgst'])
        invdata.sgst=float(request.POST['sgst'])
        invdata.igst=float(request.POST['igst'])
        invdata.othercharges=float(request.POST['other-charge'])
        invdata.roundoff=float(request.POST['roundoff'])
        invdata.discountcharge=float(request.POST['discount'])
        invdata.totalcharges=float(request.POST['total'])
        invdata.created_by=request.user
        invdata.updated_by=request.user
        invdata.save()
        return redirect('gridInvoice')



    else:
        invcount=InvoiceManagement.objects.all().count()
        invdate=date.today()
        
        if invcount > 0:
            invno=InvoiceManagement.objects.last()
            newinvno="SC/INV/"+str(invno.countervalue+1)
        else:
            newinvno="SC/INV/1"
        context={'invno':newinvno,"invdate":invdate,"nopack":1}
        
        
        return render(request, 'shravanmanagemet/shravancare_invoice_details_manage.html', context)




@login_required(login_url='manage_login')
def editInvoice(request,pk):
    invdata=InvoiceManagement.objects.get(id=pk)
    context={'invdata':invdata,'disabled':'disabled'}
    if request.method == 'POST':
        
        invdata.invdescribe=request.POST['invoice-desc']
        invdata.subtotal=float(request.POST['rate'])
        invdata.gstpercentage=float(18)
        invdata.gstamount=float(request.POST['cgst'])+float(request.POST['sgst'])
        invdata.cgst=float(request.POST['cgst'])
        invdata.sgst=float(request.POST['sgst'])
        invdata.igst=float(request.POST['igst'])
        invdata.othercharges=float(request.POST['other-charge'])
        invdata.roundoff=float(request.POST['roundoff'])
        invdata.discountcharge=float(request.POST['discount'])
        invdata.totalcharges=float(request.POST['total'])
        invdata.created_by=request.user
        invdata.updated_by=request.user
        invdata.save()
        
        
        
        return redirect('gridInvoice')

    
    
    return render(request, 'shravanmanagemet/shravancare_invoice_details_manage.html', context)



@login_required(login_url='manage_login')
def viewInvoice(request,pk):
    invdata=InvoiceManagement.objects.get(id=pk)
    context={'invdata':invdata,'view':'disabled'}
    
    
    return render(request, 'shravanmanagemet/shravancare_invoice_details_manage.html', context)


@login_required(login_url='manage_login')
def gridInvoice(request):

    invoice=InvoiceManagement.objects.all()
    context={'invoice':invoice}    
    
    return render(request, 'shravanmanagemet/shravancare_invoice_details_grid.html', context)


def homePageDataBeforeLogin(request):
    if request.user.is_authenticated:

        banners=HomePageSlider.objects.all().order_by('position')
        slot=Slots.objects.all()
        testimonials=Testimonials.objects.all().order_by('position')
        country=Country.objects.all()
        userdetail=User_Profile.objects.get(user=request.user)
        elderdetail=Elder_Details.objects.get(user_id=userdetail.user)
        customerparents=Customer_Parents.objects.filter(user_id=userdetail.user)
        invmanage=InvoiceManagement.objects.filter(cust_id=request.user.id)
        visitdetails=IcareVisitScheduling.objects.filter(cust_id=request.user.id).order_by('visitdate')
        todaysdateis=date.today()
        tomorrowsdateis=todaysdateis + datetime.timedelta(days=1)
        
        
        context={'banners':banners,"todaysdateis":todaysdateis,"tomorrowsdateis":tomorrowsdateis,"visitdetails":visitdetails,"invmanage":invmanage,'customerparents':customerparents,'testimonials':testimonials,'userdetail':elderdetail,'elderdetail':elderdetail,'country':country,"slot":slot}
        return render(request, 'shravanmanagemet/index.html', context)
    else:
        
        banners=HomePageSlider.objects.all().order_by('position')
        testimonials=Testimonials.objects.all().order_by('position')
        country=Country.objects.all()
        
        
        context={'banners':banners,'testimonials':testimonials,'country':country}
        return render(request, 'shravanmanagemet/index.html', context)


def custRegister(request):
    if request.method == 'POST':
        countryinst=Country.objects.get(id=request.POST['country'])
        stateinst=State.objects.get(id=request.POST['state'])
        cityinst=City.objects.get(id=request.POST['city'])
        countryinstelder=Country.objects.get(id=request.POST['elder-country'])
        stateinstelder=State.objects.get(id=request.POST['elder-state'])
        cityinstelder=City.objects.get(id=request.POST['elder-city'])
        pincodeinstelder=Pincode.objects.get(id=request.POST['elder-pincode'])
        custcreate = CustomUser.objects.create(is_customer=True,username=request.POST['email'],email=request.POST['email'],is_staff=False,is_superuser=False,password=make_password("1234"),is_active=True) 
        custcreate.save()
        custprofile=User_Profile.objects.create(user=custcreate)
        custprofile.name= request.POST['fname']
        custprofile.address= request.POST['addr']
        custprofile.mobile= request.POST['phone']
        custprofile.country= countryinst
        custprofile.state= stateinst
        custprofile.city= cityinst
        custprofile.save()
        countlen=len(request.POST.getlist('elder-name[]'))
        parentname=request.POST.getlist('elder-name[]')
        parentage=request.POST.getlist('elder-age[]')
        parentgender=request.POST.getlist('elder-gender[]')
        
        for x in range(0,countlen):
            custparent=Customer_Parents.objects.create(user_id=custcreate)
            custparent.parent_name=parentname[x]
            custparent.age=parentage[x]
            custparent.gender=parentgender[x]
            custparent.is_active="YES"
            custparent.save()
        parentdetails=Elder_Details.objects.create(user_id=custcreate)
        parentdetails.address=request.POST['elder-addr']
        parentdetails.mobile=request.POST['elder-mob']
        parentdetails.country=countryinstelder
        parentdetails.state=stateinstelder
        parentdetails.city=cityinstelder
        parentdetails.pincode=pincodeinstelder
        parentdetails.save()
        
        banners=HomePageSlider.objects.all().order_by('position')
        testimonials=Testimonials.objects.all().order_by('position')
        country=Country.objects.all()
        messagemain="Hello "+str(request.POST['fname'])+", this is your credentials- Username:"+str(request.POST['email'])+" and Password: 1234"
        send_mail("Welcome to Shravancare",messagemain,settings.EMAIL_HOST_USER,emptemp.email) 
        context={'banners':banners,'testimonials':testimonials,'country':country}
        return render(request, 'shravanmanagemet/index.html', context)

def customerLogin(request):
    if request.method == 'POST':
          username = request.POST['custemaillogin']
          password = request.POST['custpwdlogin']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active and user.is_customer:
                  profile=User_Profile.objects.get(user=user.id)
                  login(request,user)
                  request.session["name"] = profile.name
                  
                  context={}
                  return redirect('homePageDataBeforeLogin')
              else:
                  messages.error(request,"Not A Valid User")
                  return redirect('homePageDataBeforeLogin')
          else:
                messages.error(request,"Invalid username or password")
                return redirect('homePageDataBeforeLogin')
    else:
        # the login is a  GET request, so just show the user the login form.
        return redirect('homePageDataBeforeLogin')


def logout_frontend(request):
    logout(request)
    request.session.flush()
    return redirect('homePageDataBeforeLogin')



@login_required(login_url='manage_login')
def addZone(request):
    
    if request.method == 'POST':
        
        zone_name = request.POST['zonename']
        zone_describe = request.POST['zonedescrip']
           
        # creating Task Categ here
        createZone = Zone.objects.create(zone_name=zone_name, zone_describe=zone_describe) 
        
        createZone.save() 
        return redirect('gridZone')
    else:
        context={}
        
        return render(request, 'shravanmanagemet/shravancare_zone_manage.html', context)

@login_required(login_url='manage_login')
def editZone(request,pk):
    zonedetails=Zone.objects.get(id=pk)
    
    context={'zonedetails':zonedetails}
    if request.method == 'POST':
        zonedetails.zone_name = request.POST['zonename']
        zonedetails.zone_describe =request.POST['zonedescrip']        
        zonedetails.save()        
        return redirect('gridZone')
    return render(request, 'shravanmanagemet/shravancare_zone_manage.html', context)


@login_required(login_url='manage_login')
def viewZone(request,pk):
    zonedetails=Zone.objects.get(id=pk)
    context={'zonedetails':zonedetails,'view':'disabled'}
    return render(request, 'shravanmanagemet/shravancare_zone_manage.html', context)

@login_required(login_url='manage_login')
def deleteZone(request,pk):
    zonedetails=Zone.objects.get(id=pk)
    zonedetails.delete()
    return redirect('gridZone')



@login_required(login_url='manage_login')
def gridZone(request):
    zonedetails=Zone.objects.exclude(id=1)
    context={'zonedetails':zonedetails}    
    return render(request, 'shravanmanagemet/shravancare_zone_grid.html', context)

@login_required(login_url='homePageDataBeforeLogin')
def zoneSearch(request,pk):
    zonedetails=User_Profile.objects.get(user=pk)
    elderdetails=Elder_Details.objects.get(user_id=zonedetails.user)
    pincode=Pincode.objects.get(id=elderdetails.pincode.id)
    if pincode.zoneid==1:
        return HttpResponse("No Serving")
    else:        
        return HttpResponse("success")





def custSearch(request,custstr):

    custdetails=User_Profile.objects.filter(user__is_customer="True").filter(
            Q(name__icontains=custstr) | Q(mobile__icontains=custstr))
    if custdetails.exists():
        custmain = {}
        cust_records=[]
        for cust in custdetails:
            elderdets= Elder_Details.objects.get(user_id=cust.user)
            custparents= Customer_Parents.objects.filter(user_id=cust.user)
            parentnames=''
            delim = '-'
            for parents in custparents:
                parentnames+= (parents.parent_name + delim) 

            record = {"custid":cust.user.id,"name":cust.name,"email":cust.user.email, "custcity":cust.city.city_name,"custaddr":cust.address,"custmobile":cust.mobile,"eldercontact":elderdets.mobile,"elderpincode":elderdets.pincode.id,"custparents":parentnames[:-1],"parentsaddr":elderdets.address}
            
            cust_records.append(record)
            

        custmain["cust"]=cust_records

        


        return JsonResponse(custmain)
    else:
        return HttpResponse("No Such Customer")

def viewCustInvoice(request,pk):
    
    invdetails=InvoiceManagement.objects.get(id=pk)
    if invdetails:

    
        context={'invdetails':invdetails}
        
        return render(request, 'shravanmanagemet/shravancare_invoice.html', context)
    else:
        return redirect('errorPage')


def errorPage(request):
    context={}
    return render(request, 'shravanmanagemet/error-page.html', context)




@login_required(login_url='homePageDataBeforeLogin')
def myProfile(request):
    customer=User_Profile.objects.get(user=request.user)
    eldernames=Customer_Parents.objects.filter(user_id=request.user)
    parentsdets=Elder_Details.objects.get(user_id=request.user)
    country=Country.objects.all()
    state=State.objects.filter(country=customer.city.state.country)
    city=City.objects.filter(state=customer.city.state)
    
    state1=State.objects.filter(country=parentsdets.pincode.city.state.country)
    city1=City.objects.filter(state=parentsdets.pincode.city.state)
    
    pincode=Pincode.objects.filter(city=parentsdets.pincode.city)
    

    try:
        customerpassport=Cust_ID_Proof.objects.get(user_id=customer.user)
    except Cust_ID_Proof.DoesNotExist:
        customerpassport = Cust_ID_Proof.objects.create(user_id=customer.user)
    
    if request.method == 'POST':

        countryinst=Country.objects.get(id=request.POST['cli-country'])
        stateinst=State.objects.get(id=request.POST['cli-state'])
        cityinst=City.objects.get(id=request.POST['cli-city'])
        countryinstelder=Country.objects.get(id=request.POST['elder-country'])
        stateinstelder=State.objects.get(id=request.POST['elder-state'])
        cityinstelder=City.objects.get(id=request.POST['elder-city'])
        pincodeinstelder=Pincode.objects.get(id=request.POST['elder-pincode'])
        
        customer.name= request.POST['cli-name']
        customer.address= request.POST['cli-addr']
        customer.mobile= request.POST['cli-mob']
        customer.country= countryinst
        customer.state= stateinst
        customer.city= cityinst
        if request.FILES['cust-profile-upload-input']:
            custprofile= request.FILES['cust-profile-upload-input']
            
            fs4 = FileSystemStorage()
            filename4 = fs4.save(custprofile.name, custprofile)
            profileurl = fs4.url(filename4)
            customer.profilepic=profileurl
        customer.save()
        if request.FILES['cust-passport-upload-input']:
            custpassport= request.FILES['cust-passport-upload-input']
            customerpassport.passportnumber= request.POST['passport']
            fs3 = FileSystemStorage()
            filename3 = fs3.save(custpassport.name, custpassport)
            passport = fs3.url(filename3)
            customerpassport.passporturl=passport
        customerpassport.save()
        
        countlen=len(request.POST.getlist('elder-name[]'))
        parentname=request.POST.getlist('elder-name[]')
        parentage=request.POST.getlist('elder-age[]')
        parentgender=request.POST.getlist('elder-gender[]')
        parentadhaar=request.POST.getlist('elder-aadharno[]')
        profileelder = request.FILES.getlist('elder-profile-upload-input[]')
        adhaarelder = request.FILES.getlist('elder-adhaar-upload-input[]')
        eldernames.delete()
        
        for x in range(0,countlen):
            custparent=Customer_Parents.objects.create(user_id=customer.user)
            custparent.parent_name=parentname[x]
            custparent.age=parentage[x]
            custparent.gender=parentgender[x]
            custparent.adhaarnumber=parentadhaar[x]
            custparent.is_active="YES"
            if profileelder[x]:
                fs = FileSystemStorage()
                filename = fs.save(profileelder[x].name, profileelder[x])
                profilepic = fs.url(filename)
                custparent.adhaarurl=profilepic
            if adhaarelder[x]:
                fs2 = FileSystemStorage()
                filename2 = fs2.save(adhaarelder[x].name, adhaarelder[x])
                adhaarpic = fs2.url(filename2)
                
                custparent.profileurl=adhaarpic
            custparent.save()
        
        parentsdets.address=request.POST['elder-addr']
        parentsdets.mobile=request.POST['elder-mob']
        parentsdets.country=countryinstelder
        parentsdets.state=stateinstelder
        parentsdets.city=cityinstelder
        parentsdets.pincode=pincodeinstelder
        parentsdets.description=request.POST['med-inst']
        parentsdets.save()
        return redirect('homePageDataBeforeLogin')

    

    context={'customer':customer,"state1":state1,"city1":city1,"customerpassport":customerpassport,'eldernames':eldernames,'parentsdets':parentsdets,"country":country,"state":state,"city":city,"pincode":pincode}
        
    return render(request, 'shravanmanagemet/shravancare_update_profile.html', context)




def icareAvailableSlot(request,icare,slotid,visdate):

    count=IcareVisitScheduling.objects.filter(slot_id__id=slotid,icare_id=icare,visitdate=visdate).count()
    if count==1:
        return HttpResponse("Booked")
    else:        
        return HttpResponse("Empty")


@login_required(login_url='homePageDataBeforeLogin')
def checkavailableIcare(request):
    
    icare_records=[]
    
    if request.method == 'POST':

        reqmonth=request.POST['month-duration']
        reqstart=request.POST['formdate']
        reqend=request.POST['toodate']
        reqplantype=request.POST['Sel-plan']
        reqweek=request.POST['week-prefer-option']
        reqday=request.POST['day-prefer-option']
        reqslot=request.POST['slot-prefer-option']
        userdetail=User_Profile.objects.get(user=request.user)
        elderdetail=Elder_Details.objects.get(user_id=userdetail.user)
        customerparents=Customer_Parents.objects.filter(user_id=userdetail.user)
        slot=Slots.objects.all()
        
        listofIcareaccordingtozone=User_Profile.objects.filter(user__is_icare=True).filter(pincode_id=elderdetail.pincode)
        if listofIcareaccordingtozone.count() > 0:
            for icare in listofIcareaccordingtozone:
                availablity=InvoiceManagement.objects.filter(icareid=icare.user).filter(startdate__gte = reqstart).filter(enddate__lte = reqend).filter(plantype=reqplantype).filter(preferedday=reqday).filter(preferedweek=reqweek).filter(slotid__id=reqslot).count()
                if availablity == 0:
                    icare_records.append(icare)
            context={"icare_records":icare_records,"slot":slot,"reqmonth":reqmonth,"reqstart":reqstart,"reqend":reqend,"reqplantype":reqplantype,"reqweek":reqweek,"reqday":reqday,"reqslot":reqslot,"userdetail":userdetail,"elderdetail":elderdetail,"customerparents":customerparents}
            return render(request, 'shravanmanagemet/sharavancare_select_icarepartner.html', context)
            
        else:
            context={"icare_records":"None Available","slot":slot,"reqmonth":reqmonth,"reqstart":reqstart,"reqend":reqend,"reqplantype":reqplantype,"reqweek":reqweek,"reqday":reqday,"reqslot":reqslot,"userdetail":userdetail,"elderdetail":elderdetail,"customerparents":customerparents}
            return render(request, 'shravanmanagemet/sharavancare_select_icarepartner.html', context)

@login_required(login_url='homePageDataBeforeLogin')
def save_package(request):
    ajaxdata=json.loads(request.POST['maindata'])
    
    if request.method == 'POST':
        gstcharge=round(((18/100)*(int(ajaxdata['cost']))),2)
        invcount=InvoiceManagement.objects.all().count()
        invdate=date.today()
        
        if invcount > 0:
            invno=InvoiceManagement.objects.last()
            newinvno="SC/INV/"+str(invno.countervalue+1)
        else:
            newinvno="SC/INV/1"
        
        userdetail=User_Profile.objects.get(user=request.user)
        elderdetail=Elder_Details.objects.get(user_id=userdetail.user)
        customerparents=Customer_Parents.objects.filter(user_id=userdetail.user)
        parentnames=''
        delim = '-'
        for parents in customerparents:
            parentnames+= (parents.parent_name + delim)

        packagedescription="Plan Type:"+str(ajaxdata['plan'])+" For - "+str(ajaxdata['months'])+" Months. Start Date:"+str(ajaxdata['fromdate'])+", End Date: "+str(ajaxdata['todate'])+" Total Visits:"+str(ajaxdata['visit'])
        
        invdata=InvoiceManagement.objects.create(invoiceno=newinvno)
        invdata.countervalue=invcount+1
        invdata.invdate=invdate
        invdata.cust_id=CustomUser.objects.get(id=userdetail.user.id) 
        invdata.custname=userdetail.name
        invdata.custaddr=userdetail.address
        invdata.custcity=City.objects.get(id=userdetail.city.id) 
        invdata.eldersname=parentnames
        invdata.elderpincode=Pincode.objects.get(id=elderdetail.pincode.id)
        invdata.elderaddr=elderdetail.address
        invdata.eldercontact=elderdetail.mobile
        invdata.custcontact=userdetail.mobile
        invdata.invdescribe=packagedescription
        invdata.invoicetype="Package"
        invdata.plantype=ajaxdata['plan']
        invdata.preferedweek=ajaxdata['prefweek']
        invdata.preferedday=ajaxdata['prefday']
        invdata.icareid=CustomUser.objects.get(id=ajaxdata['icare'])
        invdata.slotid=Slots.objects.get(id=ajaxdata['prefslot'])
        invdata.numberofvisits=ajaxdata['visit']
        invdata.numberofmonths=ajaxdata['months']
        
        invdata.subtotal=float(ajaxdata['cost'])
        invdata.gstpercentage=float(18)
        invdata.gstamount=gstcharge
        invdata.cgst=float(0.00)
        invdata.sgst=float(0.00)
        invdata.igst=float(gstcharge)
        invdata.othercharges=float(0.00)
        invdata.roundoff=float(0.00)
        invdata.discountcharge=float(0.00)
        invdata.totalcharges=float(int(ajaxdata['cost'])+gstcharge)
        invdata.created_by=request.user
        invdata.updated_by=request.user
        invdata.enddate=ajaxdata['todate']

        invdata.startdate=ajaxdata['fromdate']
        invdata.save()
        for vis in ajaxdata['appointments']:
            visdata=IcareVisitScheduling.objects.create(slot_id=Slots.objects.get(id=ajaxdata['prefslot']),custparentname=parentnames,custparentaddr=elderdetail.address,cust_id=CustomUser.objects.get(id=userdetail.user.id) ,icare_id=CustomUser.objects.get(id=ajaxdata['icare']),visitdate=vis,visitstatus="Not Confirmed",created_by=request.user,updated_by=request.user)
            visdata.save()
        return HttpResponse("Success")


@login_required(login_url='homePageDataBeforeLogin')
def visitRescheduleSave(request,visitid,icare,slotid,visdate):
    visitdata=IcareVisitScheduling.objects.get(id=visitid)
    visitdata.visitdate=visdate
    visitdata.slot_id=Slots.objects.get(id=slotid)
    visitdata.icare_id=CustomUser.objects.get(id=icare)
    visitdata.save()
    return HttpResponse("Success")
    


def savePendingTasks(request):
    ajaxdata=json.loads(request.POST.get('maindata1'))
    for ajax in ajaxdata:
        taskdata=PendingTasks.objects.create(visitid=IcareVisitScheduling.objects.get(id=ajax['visit_id']),taskid=Task.objects.get(id=ajax['taskid']),amount=ajax['amount'],remark=ajax['remarks'],duedate=ajax['due-date'],notifyadmin=ajax['gridCheck1'])
        fs2 = FileSystemStorage()
        filename2 = fs2.save(ajax['files'].name, ajax['files'])
        taskfilemain = fs2.url(filename2)
        taskdata.taskfile=taskfilemain
        taskdata.save()
        visdataupdate=IcareVisitScheduling.objects.get(id=ajax['visit_id'])
        visdataupdate.visitstatus="Visited"
        visdataupdate.save()

        return HttpResponse("Success")


def customerSupportCreate(request):
    if request.user.is_authenticated:
        custsupport=Customer_Request.objects.create(ticketno=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        custsupport.is_customer=CustomUser.objects.get(id=request.user.id)
        custsupport.custname=request.POST['ccname']
        custsupport.custemail=request.POST['ccemail']
        custsupport.custmobile=request.POST['ccmob']
        custsupport.query_description =request.POST['ccmsg']
        custsupport.reqtype='CUSTOMER SUPPORT'
        custsupport.save()
        messages.error(request,"Support Executive Will Get Back To You")
        return redirect('homePageDataBeforeLogin')
    else:
        messages.error(request,"Login First")
        return redirect('homePageDataBeforeLogin')


def salesCreate(request):
    
    custsupport=Customer_Request.objects.create(ticketno=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    custsupport.custname=request.POST['csname']
    custsupport.custemail=request.POST['csemail']
    custsupport.custmobile=request.POST['csmob']
    custsupport.query_description =request.POST['csmsg']
    custsupport.save()
    messages.error(request,"Sales Person Will Get Back To You")
    return redirect('homePageDataBeforeLogin')

@login_required(login_url='manage_login')
def updatePendingTask(request,pk):
    updatepending=PendingTasks.objects.get(id=pk)
    updatepending.taskstatus="Completed"
    updatepending.save()
    return redirect('shravanCareDashboard')




       
    