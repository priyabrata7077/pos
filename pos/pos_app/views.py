import datetime
from django.dispatch import receiver
from rest_framework.permissions import BasePermission
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from rest_framework.decorators import api_view
from .serializer import *
from django.contrib.auth import logout
from rest_framework import generics, permissions
from rest_framework import status, generics,permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            # Retrieve employee data
            employee = EmployeeMaster.objects.get(username=username)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
@login_required
def current_user(request):
    user = request.user
    # You can customize which user fields you want to include in the response
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        # Add more fields as needed
    }
    return JsonResponse(user_data)
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UnitListView(generics.ListCreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class BrandListView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CompanyListView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ItemListView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
class BusinessDetailView(generics.RetrieveUpdateAPIView):
    queryset = business.objects.all()
    serializer_class = BusinessSerializer
    lookup_field = 'owner'
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Owner.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                })
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Owner.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
class BusinessListCreateView(generics.ListCreateAPIView):
    queryset = business.objects.all()
    serializer_class = BusinessSerializer

class BusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = business.objects.all()
    serializer_class = BusinessSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class CustomUserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = CustomUserSerializer
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({"success": "Successfully logged out"})
class HomeView(APIView):
    permission_classes = ()

    def get(self, request):
        print(request.META.get('HTTP_AUTHORIZATION'))
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = business.objects.all()
    serializer_class = BusinessSerializer
def update_stock_on_purchase(sender, instance, created, **kwargs):
    if created:  # This ensures the signal is only triggered on new purchase records
        try:
            stock_item = StockRegister.objects.get(itembarcode=instance.itembarcode1)
            stock_item.itemqty += instance.itemqty  # Assuming puritemqty is the field representing the purchase quantity
            stock_item.save()
        except StockRegister.DoesNotExist:
            # Handle scenario where the stock item doesn't exist
            pass
@receiver(post_save, sender=SalesRegister1)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if created:  # This ensures the signal is only triggered on new sales records
        try:
            stock_item = StockRegister.objects.get(itembarcode=instance.itembarcode1)
            if stock_item.itemqty >= instance.itemqty:
                stock_item.itemqty -= instance.itemqty
                stock_item.save()
            else:
                # Handle insufficient stock scenario
                # Maybe raise an exception or log the error
                pass
        except StockRegister.DoesNotExist:
            # Handle scenario where the stock item doesn't exist
            pass
class PurchasePendingViewSet(viewsets.ModelViewSet):
    queryset = PurchasePending.objects.all()
    serializer_class = PurchasePendingSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    
  
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'barcode'
    
class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
class TransactionDetailView(generics.CreateAPIView):
    
    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        return JsonResponse({'message': 'Transaction deleted successfully.'}, status=204)
class StockRegisterViewSet(viewsets.ModelViewSet):
    queryset = StockRegister.objects.all()
    serializer_class = StockRegisterSerializer
    lookup_field = 'itembarcode'  
    def get(self, request, *args, **kwargs):
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        # Check if both start_date and end_date are provided
        if start_date and end_date:
            sales_data = StockRegister.objects.filter(created_at__range=[start_date, end_date]).values()
        else:
            # If not provided, return all data
            sales_data = StockRegister.objects.values()

        # Example: Calculate total amount for the given date range
        total_amount = StockRegister.objects.filter(created_at__range=[start_date, end_date]).aggregate(Sum('amount'))

        return JsonResponse({'sales_data': list(sales_data), 'total_amount': total_amount})  
class SalesRegister1ViewSet(viewsets.ModelViewSet):
    serializer_class = SalesRegister1Serializer
    queryset = SalesRegister1.objects.all()
    @action(detail=False, methods=['GET'])
    def date_filtered_sales(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        print('start_date:', start_date)
        print('end_date:', end_date)

        if not start_date or not end_date:
            return Response({'error': 'Both start_date and end_date are required.'}, status=400)

        try:
            queryset = SalesRegister1.objects.filter(
                created_at__gte=datetime.strptime(start_date, '%Y-%m-%d'),
                created_at__lte=datetime.strptime(end_date, '%Y-%m-%d')
            )

            serializer = SalesRegister1Serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            print('Error:', e)
            return Response({'error': 'An error occurred while processing the request.'}, status=500)
     
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = customers.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'custmob'
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class IsEmployeeSameBusiness(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has an associated employee object
        if request.user.is_authenticated and hasattr(request.user, 'employee'):
            # Check if the logged-in user's employee instance is associated with the same business as the accessed employee
            return obj.business == request.user.employee.business
        return False  # Return False if the user is not authenticated or does not have an associated employee object

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsEmployeeSameBusiness]
    lookup_field = 'username'
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .models import Item
@receiver(post_save, sender=EmployeeMaster)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        # Create a new User instance
        user = User.objects.create(
            username=instance.username,
            is_staff=True,
            is_active=True
        )
        # Set the password using make_password
        user.set_password(instance.password)
        # Set the business field of the User to the corresponding business of EmployeeMaster
        user.business = instance.business
        user.save()
    else:
        # Update an existing User instance
        user = instance.user  # Assuming there is a OneToOneField named 'user' linking EmployeeMaster to User
        if user:
            user.username = instance.username
            user.set_password(instance.password)
            # Update the business field of the User to the corresponding business of EmployeeMaster
            user.business = instance.business
            user.save()    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_view_items(request, item_id):
    user_business = request.user.owner.business
    item = get_object_or_404(Item, id=item_id, business=user_business)

    return JsonResponse({'itemname': item.itemname})
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    

    @action(detail=True, methods=['put'])
    def update_item_unit(self, request, pk=None):
        try:
            item = self.get_object() 
            new_unit = request.data.get('itemunit') 
            
            if new_unit is not None:  
                item.itemunit = new_unit
                item.save()
                return Response({'message': 'Item unit updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'itemunit value is required'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Item.DoesNotExist:
            return Response({'error': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class SalesPendingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on SalesPending model.
    """
    
    queryset = SalesPending.objects.all()  
    serializer_class = SalesPendingSerializer 
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle updating SalesPending instance.
        """
        instance = self.get_object()  
        serializer = self.get_serializer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to handle deleting SalesPending instance.
        """
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    def perform_destroy(self, instance):
        """
        Method to perform actual deletion of the SalesPending instance.
        """
        instance.delete()  

class TransactionDetailsViewSet(viewsets.ModelViewSet):
    queryset = transaction_details.objects.all()
    serializer_class = TransactionDetailsSerializer
class PurchaseDetailsViewSet(viewsets.ModelViewSet):
    queryset = purchasedetails1.objects.all()  
    serializer_class = PurchaseDetailsSerializer 

class PurchaseRegisterViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRegister1.objects.all() 
    serializer_class = PurchaseRegisterSerializer 

class AccountsMasterViewSet(viewsets.ModelViewSet):
    queryset = AccountsMaster1.objects.all()
    serializer_class = AccountsMasterSerializer
    lookup_field = 'accmob'
def get_item_name(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        return JsonResponse({'itemname': item.itemname})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)