from django.db import models
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class Brand(models.Model):
    business_id = models.ForeignKey('business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Attribute_options (models.Model):
    business_id = models.ForeignKey('business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Attribute (models.Model):
    business_id = models.ForeignKey('business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Company(models.Model):
    business_id = models.ForeignKey('business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Unit(models.Model):
    business_id = models.ForeignKey('business', on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=255)
    si_unit = models.CharField(max_length=50)
    unit_to_kg = models.DecimalField(max_digits=10, decimal_places=4)
    unit_to_gram = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unit_name
class Category(models.Model):
    business_id = models.ForeignKey('business', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cat_parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Owner(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # If username and password are not set, use default values
        if not self.username:
            self.username = f"default_username_{self.id}"

        if not self.password:
            self.password = make_password(f"default_password_{self.id}")

        # Call the superclass save method to save the object
        super().save(*args, **kwargs)

        # Create or update the associated user
        User = get_user_model()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_active = True  # Ensure the user is active
        user.save()

        # Set the owner attribute of the user
        user.owner = self
        user.save()

        # Add the user to the "owner" group
        owner_group, created = Group.objects.get_or_create(name='Owner')
        owner_group.user_set.add(user)

class CustomUser(models.Model):
    USER_TYPES = (
        ('Owner', 'Owner'),
        ('Business', 'Business'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='Business')
    phone = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.username
class Transaction(models.Model):
    business = models.ForeignKey('business', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=25, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)
    bill_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    card_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paytm_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    credit_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance_return = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.mobile_number}"
class StockRegister(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    osid = models.CharField(blank=True, null=True, max_length=10)
    itemid = models.ForeignKey('Item', on_delete=models.CASCADE,blank=True, null=True,)
    itemqty = models.IntegerField(blank=True, null=True)
    purrate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemmrp = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemsalerate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itembarcode = models.IntegerField(
        unique=True, 
        blank=True,
        null=True,
    )
    locid = models.CharField(blank=True, null=True, max_length=10)
    def get_item_name(self):
        return self.itemid.itemname

    def __str__(self):
        return f"{self.osid} - {self.get_item_name()}"
    
class SalesRegister1(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    salesregisSNo = models.IntegerField(blank=True, null=True)
    billnum = models.CharField(max_length=50, blank=True, null=True)
    itemname = models.CharField(max_length=50, blank=True, null=True)
    itemqty = models.IntegerField(blank=True, null=True)
    itembarcode1 = models.CharField(max_length=50, blank=True, null=True)
    itemrate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    itemmrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    itempurrate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    itemtaxrate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    othrchrgs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    othrdisc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    billtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    custid = models.IntegerField(blank=True, null=True)
    locid = models.IntegerField(blank=True, null=True)
    saletime = models.DateTimeField(blank=True, null=True)
    empid = models.IntegerField(blank=True, null=True)
    mopcash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mopcard = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    moppaytm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mopcreditsale = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
class PurchasePending(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    accid = models.IntegerField(blank=True, null=True)
    purbillno = models.CharField(blank=True, null=True, max_length=30)
    itemid = models.IntegerField(blank=True, null=True)
    puritemqty = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itembarcode1 = models.CharField(blank=True, null=True, max_length=50)
    purrate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemname = models.CharField(max_length=50, blank=True, null=True)
    itemmrp = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemsalerate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemtaxid = models.CharField(blank=True, null=True, max_length=10)
    empid = models.IntegerField(blank=True, null=True)
    locid = models.IntegerField(blank=True, null=True)
    def __str__(self):
        itemrowtotal_value = self.purrate * self.puritemqty if self.purrate and self.puritemqty else 0
        return f"{self.itemname} - Total Amount: {itemrowtotal_value}"
    def __str__(self):
        return self.itemname 
    def __str__(self):
        return f"{self.purbillno} - {self.itemid} - {self.itemname} "
class customers(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    custname = models.CharField(max_length=255)
    custmob = models.PositiveBigIntegerField(unique=True)
    custadd1 = models.TextField()
    custadd2 = models.TextField(blank=True, null=True)  # Optional
    custgloclat = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    custgloclang = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    custemail = models.EmailField(blank=True, null=True)
    custcnum = models.CharField(blank=True, null=True, max_length=50)
    custctype = models.CharField (blank=True, null=True, max_length=50)
    custcompname = models.CharField(blank=True, null=True, max_length=255)
    custallowcr = models.BooleanField(blank=True, null=True, default=False)
    custaccount = models.CharField(blank=True, null=True, max_length=50)
    custaccid = models.CharField(blank=True, null=True, max_length=50)
    custpincode = models.CharField(max_length=10, blank=True, null=True)
    custgstin = models.CharField(blank=True, null=True, max_length=50)
    custtype = models.CharField(blank=True, null=True, max_length=50)
    custbdate = models.DateField(blank=True, null=True, )
    custlocid = models.CharField(blank=True, null=True, max_length=50)  # Optional

    def __str__(self):
        return self.custname if self.custname else 'Unnamed Customer'
class Item(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE)
    itemid = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=255)
    itemunit = models.ForeignKey(Unit,on_delete=models.CASCADE,blank=True, null=True,)
    itemcatid = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True, null=True,)
    itemgrpid = models.IntegerField()
    itemsgrpid = models.IntegerField()
    itemtaxid = models.IntegerField()
    itemhsn = models.CharField(max_length=20)
    itemmrp = models.DecimalField(max_digits=10, decimal_places=2)
    itemmasterproductid = models.CharField(max_length=50)
    itemcasesize = models.CharField(max_length=50)
    itemshell = models.CharField(max_length=50)
    itemtype = models.CharField(max_length=50)
    itemdesc = models.TextField()
    itembarcode1 = models.CharField(max_length=50)
    itembarcode2 = models.CharField(max_length=50)
    itembarcode3 = models.CharField(max_length=50)
    itembrand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True, null=True,)
    itemcompany = models.ForeignKey(Company,on_delete=models.CASCADE,blank=True, null=True,)
    Attributes= models.ForeignKey(Attribute,on_delete=models.CASCADE,blank=True, null=True,)
    Attributes_options= models.ForeignKey(Attribute_options,on_delete=models.CASCADE,blank=True, null=True,)
    def __str__(self):
        return self.itemname
class SalesPending(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    locid = models.IntegerField(blank=True, null=True)
    empid = models.IntegerField(blank=True, null=True)
    itemid = models.IntegerField(blank=True, null=True)
    itembarcode1 = models.CharField(blank=True, null=True, max_length=50)
    itemname = models.CharField(blank=True, null=True, max_length=255)
    itemmrp = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itempurrate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemrate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    itemqty = models.IntegerField(blank=True, null=True)
    itemgst = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    itemrowtotal = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    def __str__(self):
        itemrowtotal_value = self.itemrate * self.itemqty if self.itemrate and self.itemqty else 0
        return f"{self.itemname} - Total Amount: {itemrowtotal_value}"
    def __str__(self):
        return self.itemname 
    
class transaction_details(models.Model):
    title = models.CharField(max_length=100) 
class purchasedetails1(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    purdetSNo = models.IntegerField(primary_key=True)
    purid = models.IntegerField(blank=True, null=True,)
    purbillno = models.CharField(max_length=30, null=True, blank=True)
    itemid = models.IntegerField(blank=True, null=True)
    puritemqty = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2)
    purrate = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2)
    itemmrp = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2)
    itemcustomcode = models.CharField(max_length=30, null=True, blank=True)
    itemsalerate = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2)
    itemtaxid = models.CharField(blank=True, null=True,max_length=12)
    def __str__(self):
        return f"Purchase {self.purbillno} - Item ID: {self.itemid}"
class PurchaseRegister1(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    purid = models.IntegerField(null=True, blank=True)
    accid = models.IntegerField(null=True, blank=True)
    purbillno = models.CharField(null=True, blank=True, max_length=30)
    purbilldate = models.DateField(null=True, blank=True)
    itemqty = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2)
    othrchrgs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    othrdisc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    freight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    locid = models.CharField(null=True, blank=True, max_length=30)
    entrytime = models.TimeField(null=True, blank=True)
    empid = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"Purchase Register Entry {self.purbillno} - ID: {self.id}"

class AccountsMaster1(models.Model):
    business = models.ForeignKey('business',on_delete=models.CASCADE,blank=True, null=True,)
    accid = models.IntegerField(null=True, blank=True)
    accname = models.CharField(null=True, blank=True, max_length=120)
    accgid = models.IntegerField(null=True, blank=True)
    accbillwise = models.BooleanField(null=True, blank=True)
    acccreperiod = models.IntegerField(null=True, blank=True)
    acccrelimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    accadd1 = models.CharField(max_length=220, null=True, blank=True)
    accadd2 = models.CharField(max_length=30, null=True, blank=True)
    acccity = models.CharField(max_length=30, null=True, blank=True)
    accpincode = models.IntegerField(null=True, blank=True)
    accgstin = models.CharField(max_length=15, null=True, blank=True)
    accgloclat = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    accgloclang = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    accmob = models.PositiveIntegerField(unique=True, null=True, blank=True)
    accphone = models.CharField(max_length=10, null=True, blank=True)
    accemail = models.CharField(max_length=120, null=True, blank=True)
    accoppbal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Account {self.accname} - ID: {self.accid}"
class EmployeeMasterManager(models.Manager):
    def for_user(self, user):
        if user.is_authenticated:
            return self.filter(business=user.employee.business)
        else:
            return self.none()

class EmployeeMaster(models.Model):
    group = models.ForeignKey(Group, default='Employee', on_delete=models.CASCADE)
    business = models.ForeignKey('business', on_delete=models.CASCADE)
    empid = models.AutoField(primary_key=True)
    empname = models.CharField(max_length=255, blank=True, null=True)
    empmobile = models.CharField(max_length=15, blank=True, null=True)
    empaddress = models.TextField(blank=True, null=True)
    empbankname = models.CharField(max_length=255, blank=True, null=True)
    empifsc = models.CharField(max_length=11, blank=True, null=True)
    empbankaccno = models.CharField(max_length=50, blank=True, null=True)
    emprole = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    locid = models.IntegerField(blank=True, null=True)

    objects = EmployeeMasterManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"username_{self.empid}"

        if not self.password:
            self.password = make_password(f"password_{self.empid}")

        super(EmployeeMaster, self).save(*args, **kwargs)

        try:
            group, created = Group.objects.get_or_create(name='Employee')

            user, created = User.objects.get_or_create(username=self.username)
            user.set_password(self.password)
            user.is_staff = True
            user.is_active = True
            user.business_id = self.business_id  # Set the business ID here
            user.save()

            user.groups.add(group)

        except ObjectDoesNotExist as e:
            pass

    def __str__(self):
        return self.empname

    def get_business_data(self):
        return business.objects.filter(id=self.business_id)
class business(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - Owner: {self.owner.username}" if self.name else f"Unnamed Business - Owner: {self.owner.username}"

