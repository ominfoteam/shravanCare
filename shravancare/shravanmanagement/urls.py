"""shravancare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

#from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('manage_login', views.manage_login, name="manage_login"),
    path('addTaskCategory', views.addTaskCategory, name="addTaskCategory"),
    path('addTask', views.addTask, name="addTask"),
    path('gridTaskCategory', views.gridTaskCategory, name="gridTaskCategory"),
    path('gridTask', views.gridTask, name="gridTask"),
    path('editTaskCategory/<str:pk>/', views.editTaskCategory, name="editTaskCategory"),
    path('viewTaskCategory/<str:pk>/', views.viewTaskCategory, name="viewTaskCategory"),
    path('viewTask/<str:pk>/', views.viewTask, name="viewTask"),
    path('deleteTaskCategory/<str:pk>/', views.deleteTaskCategory, name="deleteTaskCategory"),
    path('editTask/<str:pk>/', views.editTask, name="editTask"),
    path('deleteTask/<str:pk>/', views.deleteTask, name="deleteTask"),
    path('deleteSlider/<str:pk>/', views.deleteSlider, name="deleteSlider"),
    path('editSlider/<str:pk>/', views.editSlider, name="editSlider"),
    path('viewSlider/<str:pk>/', views.viewSlider, name="viewSlider"),
    path('gridSlider', views.gridSlider, name="gridSlider"),
    path('addSlider', views.addSlider, name="addSlider"),
    path('deleteTestimonial/<str:pk>/', views.deleteTestimonial, name="deleteTestimonial"),
    path('editTestimonial/<str:pk>/', views.editTestimonial, name="editTestimonial"),
    path('viewTestimonial/<str:pk>/', views.viewTestimonial, name="viewTestimonial"),
    path('gridTestimonial', views.gridTestimonial, name="gridTestimonial"),
    path('addTestimonial', views.addTestimonial, name="addTestimonial"),
    path('addEmployee', views.addEmployee, name="addEmployee"),
    path('gridEmployee', views.gridEmployee, name="gridEmployee"),
    path('gridCustomer', views.gridCustomer, name="gridCustomer"),
    path('viewCustomer/<str:pk>/', views.viewCustomer, name="viewCustomer"),
    path('editEmployee/<str:pk>/', views.editEmployee, name="editEmployee"),
    
    path('editCustomer/<str:pk>/', views.editCustomer, name="editCustomer"),
    path('gridCountry', views.gridCountry, name="gridCountry"),
    path('gridState', views.gridState, name="gridState"),
    path('gridCity', views.gridCity, name="gridCity"),
    path('gridPincode', views.gridPincode, name="gridPincode"),
    path('deleteCountry/<str:pk>/', views.deleteCountry, name="deleteCountry"),
    path('editCountry/<str:pk>/', views.editCountry, name="editCountry"),
    path('viewCountry/<str:pk>/', views.viewCountry, name="viewCountry"),
    path('viewState/<str:pk>/', views.viewState, name="viewState"),
    path('viewCity/<str:pk>/', views.viewCity, name="viewCity"),
    path('viewPincode/<str:pk>/', views.viewPincode, name="viewPincode"),
    path('addCountry', views.addCountry, name="addCountry"),
    
    #
    path('deleteState/<str:pk>/', views.deleteState, name="deleteState"),
    path('editState/<str:pk>/', views.editState, name="editState"),
    path('addState', views.addState, name="addState"),
    
    #
    path('deleteZone/<str:pk>/', views.deleteZone, name="deleteZone"),
    path('editZone/<str:pk>/', views.editZone, name="editZone"),
    path('addZone', views.addZone, name="addZone"),
    path('viewZone/<str:pk>/', views.viewZone, name="viewZone"),
    path('gridZone', views.gridZone, name="gridZone"),
    #
    path('zoneSearch/<str:pk>/', views.zoneSearch, name="zoneSearch"),
    #
    path('icareAvailableSlot/<str:icare>/<str:slotid>/<str:visdate>/', views.icareAvailableSlot, name="icareAvailableSlot"),
    path('visitRescheduleSave/<str:visitid>/<str:icare>/<str:slotid>/<str:visdate>/', views.visitRescheduleSave, name="visitRescheduleSave"),
    
    path('custSearch/<str:custstr>/', views.custSearch, name="custSearch"),
    

    #
    path('deleteCity/<str:pk>/', views.deleteCity, name="deleteCity"),
    path('editCity/<str:pk>/', views.editCity, name="editCity"),
    path('addCity', views.addCity, name="addCity"),
    
    #
    path('deletePincode/<str:pk>/', views.deletePincode, name="deletePincode"),
    path('editPincode/<str:pk>/', views.editPincode, name="editPincode"),
    path('addPincode', views.addPincode, name="addPincode"),
    path('passwordReset/<str:pk>/', views.passwordReset, name="passwordReset"),
    path('viewEmployee/<str:pk>/', views.viewEmployee, name="viewEmployee"),
    path('editEmployee/<str:pk>/', views.editEmployee, name="editEmployee"),
    #
    path('load_pincodes/',views.loadPincode, name='load_pincodes'),
	path('load_city/',views.loadCity, name='load_city'),
	path('load_state/',views.loadState, name='load_state'),
    path('logout_backend/',views.logout_backend, name='logout_backend'),
    path('icarevisit/<str:pk>/',views.icarevisit, name='icarevisit'),
    path('icaretasks/<str:pk>/',views.icaretasks, name='icaretasks'),

    #

    path('gridSalesRequest', views.gridSalesRequest, name="gridSalesRequest"),
    path('editSalesRequest/<str:pk>/', views.editSalesRequest, name="editSalesRequest"),
    path('viewSalesRequest/<str:pk>/', views.viewSalesRequest, name="viewSalesRequest"),

    #
    path('gridCustomerRequest', views.gridCustomerRequest, name="gridCustomerRequest"),
    path('editCustomerRequest/<str:pk>/', views.editCustomerRequest, name="editCustomerRequest"),
    path('viewCustomerRequest/<str:pk>/', views.viewCustomerRequest, name="viewCustomerRequest"),

    path('viewCustInvoice/<str:pk>/', views.viewCustInvoice, name="viewCustInvoice"),
    #
    path('', views.homePageDataBeforeLogin, name="homePageDataBeforeLogin"),

    path('logout_frontend', views.logout_frontend, name="logout_frontend"),
    path('customerLogin', views.customerLogin, name="customerLogin"),
    path('custRegister', views.custRegister, name="custRegister"),
    path('errorPage', views.errorPage, name="errorPage"),
    path('checkavailableIcare', views.checkavailableIcare, name="checkavailableIcare"),
    
    #
    
    path('editInvoice/<str:pk>/', views.editInvoice, name="editInvoice"),
    path('addInvoice', views.addInvoice, name="addInvoice"),
    path('viewInvoice/<str:pk>/', views.viewInvoice, name="viewInvoice"),
    path('gridInvoice', views.gridInvoice, name="gridInvoice"),
    path('myProfile', views.myProfile, name="myProfile"),
    path('save_package', views.save_package, name="save_package"),
    path('shravanCareDashboard', views.shravanCareDashboard, name="shravanCareDashboard"),
    path('savePendingTasks', views.savePendingTasks, name="savePendingTasks"), 
    path('customerSupportCreate', views.customerSupportCreate, name="customerSupportCreate"), 
    path('salesCreate', views.salesCreate, name="salesCreate"), 
    
    
    #path('', include('shravanfrontend.urls')),
    #path('api-auth/', include('rest_framework.urls'))
]
