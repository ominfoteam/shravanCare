from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid
from location.models import *

class Task_Category(models.Model):
    
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    categName=models.CharField(max_length=200,null=True, blank=True)
    categ_description = models.TextField(null=True, blank=True)
    position = models.IntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    
	

    def __str__(self):
	    return str(self.categName)

class Task(models.Model):
    STATS1=(('YES','YES'),('NO','NO'))
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    categ_id = models.ForeignKey(Task_Category, on_delete=models.CASCADE, null=True)
    taskName=models.CharField(max_length=200,null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    position = models.IntegerField(default=0)
    is_due=models.CharField(max_length=10,null=True,choices=STATS1,default='NO')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    
	

    def __str__(self):
	    return str(self.taskName)





class HomePageSlider(models.Model):
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    position=models.IntegerField(default=0)
    sliderimage=models.ImageField(default="img/Photos-new-icon.png",upload_to="slider/", null=True, blank=True)
    imagetext=models.TextField(null=True, blank=True)

    def __str__(self):
	    return str(self.imagetext)


class Testimonials(models.Model):
    
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    subtext = models.CharField(max_length=200,null=True, blank=True )
    content = models.TextField(null=True, blank=True)
    written_by=models.CharField(max_length=100,null=True, blank=True)
    position=models.IntegerField(default=0)
    
    def __str__(self):
	    return self.written_by

class CustomUser(AbstractUser):
    is_customer= models.BooleanField(default=False)
    is_icare=models.BooleanField(default=False)
    is_management=models.BooleanField(default=False)
    email = models.EmailField(unique=True)

	
class User_Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete= models.CASCADE, primary_key=True)
    name=models.CharField(max_length=50,null=True, blank=True)
    dob = models.CharField(max_length=500)
    gender = models.CharField(max_length=500)
    address = models.TextField(null=True, blank=True)
    profilepic=models.ImageField(default="img/Photos-new-icon.png",upload_to="profile_pic/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    pincode = models.ForeignKey(Pincode, on_delete=models.SET_NULL, null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='user_profile_create', on_delete=models.SET_NULL, null=True)
    updated_by=models.ForeignKey(CustomUser,related_name='user_profile_update', on_delete=models.SET_NULL, null=True)
	

    def __str__(self):
	    return self.name


class Icare_ID_Proof(models.Model):
    STATS1=(('YES','YES'),('NO','NO'))
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    id_name=models.CharField(max_length=200,null=True, blank=True)
    imgurl=models.ImageField(default="img/Photos-new-icon.png",upload_to="icareproof/", null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='icare_proof_create', on_delete=models.SET_NULL, null=True)
    is_vaccination=models.CharField(max_length=50, choices=STATS1,default='NO')
    updated_by=models.ForeignKey(CustomUser,related_name='icare_proof_update', on_delete=models.SET_NULL, null=True)
	

    def __str__(self):
	    return str(self.user_id)

class Cust_ID_Proof(models.Model):
    STATS1=(('YES','YES'),('NO','NO'))
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    passportnumber=models.CharField(max_length=200,null=True, blank=True)
    passporturl=models.ImageField(default="img/Photos-new-icon.png",upload_to="custpassport/", null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='cust_proof_create', on_delete=models.SET_NULL, null=True)
    updated_by=models.ForeignKey(CustomUser,related_name='cust_proof_update', on_delete=models.SET_NULL, null=True)
	

    def __str__(self):
	    return str(self.user_id)



class Customer_Request(models.Model):
    STATS2=(('NOT ATTENDED','NOT ATTENDED'),('IN PROCESS','IN PROCESS'),('CLOSE','CLOSE'))
    REQTYPE=(('SALES','SALES'),('CUSTOMER SUPPORT','CUSTOMER SUPPORT'))
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    ticketno=models.CharField( max_length=10,null=True, blank=True) 
    is_customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True)
    custname=models.CharField(max_length=200,null=True, blank=True)
    custemail=models.CharField(max_length=200,null=True, blank=True)
    custmobile=models.CharField(max_length=20,null=True, blank=True)
    query_description = models.TextField(null=True, blank=True)
    user_description = models.TextField(null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    querystatus=models.CharField(max_length=50, choices=STATS2,default='NOT ATTENDED')
    reqtype=models.CharField(max_length=50, choices=REQTYPE,default='SALES')
    updated_by=models.ForeignKey(CustomUser,related_name='quey_update', on_delete=models.SET_NULL, null=True)
	

    def __str__(self):
	    return str(self.custname + " - " + self.reqtype + " - "+self.querystatus)


class Customer_Parents(models.Model):
    STATS=(('YES','YES'),('NO','NO'))
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    parent_name=models.CharField(max_length=200,null=True, blank=True)
    age = models.CharField(max_length=500)
    gender = models.CharField(max_length=500)
    adhaarnumber=models.CharField(max_length=200,null=True, blank=True)
    profileurl=models.ImageField(default="img/Photos-new-icon.png",upload_to="parentprofile/", null=True, blank=True)
    adhaarurl=models.ImageField(default="img/Photos-new-icon.png",upload_to="parentadhaar/", null=True, blank=True)
    is_active=models.CharField(max_length=50, choices=STATS,default='YES')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='customer_parent_create', on_delete=models.SET_NULL, null=True)
    updated_by=models.ForeignKey(CustomUser,related_name='customer_parent_update', on_delete=models.SET_NULL, null=True)
	

    def __str__(self):
	    return str(self.user_id)



class Elder_Details(models.Model):
    
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    pincode = models.ForeignKey(Pincode, on_delete=models.SET_NULL, null=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='elder_detail_create', on_delete=models.SET_NULL, null=True)
    updated_by=models.ForeignKey(CustomUser,related_name='elder_detail_update', on_delete=models.SET_NULL, null=True)
	

    def __str__(self):
	    return str(self.user_id)

class Slots(models.Model):
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    slotname=models.CharField(max_length=200,null=True, blank=True)
    starttime=models.TimeField(null=True, blank=True)
    endtime=models.TimeField(null=True, blank=True)

    def __str__(self):
	    return str(self.slotname)

class IcareVisitScheduling(models.Model):
    
    STATSVIS=(('Not Visited','Not Visited'),('Visited','Visited'),('Not Confirmed','Not Confirmed'))
    
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    slot_id=models.ForeignKey(Slots, on_delete=models.CASCADE, null=True,related_name='slotid')
    cust_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,related_name='custforeignkey')
    icare_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,related_name='icareforeignkey')
    visitdate=models.DateField(null=True, blank=True)
    visitstatus=models.CharField(max_length=50,null=True,choices=STATSVIS,default='Not Confirmed')
    custparentname=models.TextField(null=True, blank=True)
    custparentaddr=models.TextField(null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='user_vis_create', on_delete=models.SET_NULL, null=True)
    updated_by=models.ForeignKey(CustomUser,related_name='user_vis_update', on_delete=models.SET_NULL, null=True)
	
    
	

    def __str__(self):
	    return str( self.id)





class InvoiceManagement(models.Model):
    STATSINV=(('Not Paid','Not Paid'),('Paid','Paid'))
    RENEW=(('Yes','Yes'),('No','No'))
    INVTYPE=(('Package','Package'),('Non-Package','Non-Package'))
    PLNTYPE=(('Weekly','Weekly'),('Fortnightly','Fortnightly'),('Non-Package','Non-Package'))
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    invoiceno = models.CharField(max_length=200,null=True, blank=True)
    countervalue=models.IntegerField(default=0)
    renewal=models.CharField(max_length=50,null=True,choices=RENEW,default='No')
    cust_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,related_name='user_inv_foreign')
    invdate=models.DateField(null=True, blank=True)
    custname= models.CharField(max_length=200,null=True, blank=True)
    custaddr= models.TextField(null=True, blank=True)
    custcity=models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    eldersname= models.TextField(null=True, blank=True)
    elderpincode=models.ForeignKey(Pincode, on_delete=models.SET_NULL, null=True)
    elderaddr=models.TextField(null=True, blank=True)
    eldercontact=models.TextField(null=True, blank=True)
    custcontact=models.TextField(null=True, blank=True)
    invdescribe=models.TextField(null=True, blank=True)
    invoicetype=models.CharField(max_length=50,null=True,choices=INVTYPE,default='Non-Package')
    plantype=models.CharField(max_length=50,null=True,choices=PLNTYPE,default='Non-Package')
    preferedweek=models.CharField(max_length=200,null=True, blank=True)
    preferedday=models.IntegerField(null=True,default=1)
    icareid=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,related_name='icare_inv_foreign')
    slotid=models.ForeignKey(Slots,related_name='icareslot', on_delete=models.SET_NULL, null=True)
    numberofvisits=models.IntegerField(default=0,null=True)
    numberofmonths=models.IntegerField(null=True,default=0)
    subtotal=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    gstpercentage=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    gstamount=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    cgst=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    sgst=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    igst=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    othercharges=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    roundoff=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    discountcharge=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    totalcharges=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    startdate=models.DateField(null=True, blank=True)
    enddate=models.DateField(null=True, blank=True)
    paymentstatus=models.CharField(max_length=50,null=True,choices=STATSINV,default='Not Paid')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(CustomUser,related_name='user_inv_create', on_delete=models.SET_NULL, null=True)
    updated_by=models.ForeignKey(CustomUser,related_name='user_inv_update', on_delete=models.SET_NULL, null=True)
	
    
	

    def __str__(self):
	    return str(self.invoiceno+ " - " + self.custname + " - Rs."+str(self.totalcharges))


class PendingTasks(models.Model):
    
    STATSTASK=(('Pending','Pending'),('Done','Done'))
    
    id=models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False) 
    visitid=models.ForeignKey(IcareVisitScheduling, on_delete=models.CASCADE, null=True,related_name='visitid')
    taskid=models.ForeignKey(Task, on_delete=models.CASCADE, null=True,related_name='taskforeignkey')
    amount=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    remark=models.TextField(null=True, blank=True)
    duedate=models.DateField(null=True, blank=True)
    notifyadmin=models.IntegerField(null=True,default=1)
    taskfile=models.FileField(default="",upload_to="taskfile/", null=True, blank=True)
    taskstatus=models.CharField(max_length=50,null=True,choices=STATSTASK,default='Pending')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(CustomUser,related_name='user_task_update', on_delete=models.SET_NULL, null=True)
	
    
	

    def __str__(self):
	    return str( self.id)