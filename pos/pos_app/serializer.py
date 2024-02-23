from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
def perform_create(self, serializer):
    # Set the owner field to the logged-in user
    serializer.save(owner=self.request.user)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
class CustomUserSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', read_only=True)  # Include owner_id field

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'last_login', 'is_superuser', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'date_joined', 'business_id', 'groups', 'user_permissions',
                  'owner_id'] 
    
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = business
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
class StockRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRegister
        fields = '__all__'
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be non-negative.")
        return value

    def validate(self, data):
        # Check if the context contains a DELETE request
        if self.context['request'].method == 'DELETE':
            # Add any specific delete validation logic here
            # For example, prevent deletion if the quantity is less than a certain threshold
            instance = self.instance  # Existing instance being deleted
            if instance.quantity < 10:  # Check a specific condition before deletion
                raise serializers.ValidationError("Cannot delete stock with quantity less than 10.")
        
        return data

    class Meta:
        model = StockRegister
        fields = ( 'osid','itemid', 'itemqty','purrate','itemmrp','itemsalerate','itembarcode','locid')

class SalesRegister1Serializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRegister1
        fields = '__all__'
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = customers
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
   
class PurchasePendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasePending
        fields = '__all__'
class SalesPendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPending
        fields = '__all__'

class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = transaction_details
        fields = '__all__'
class PurchaseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchasedetails1
        fields = '__all__'  
class PurchaseRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PurchaseRegister1  
        fields = '__all__'   
class AccountsMasterSerializer(serializers.ModelSerializer):
      class Meta:
        model =  AccountsMaster1  
        fields = '__all__' 
