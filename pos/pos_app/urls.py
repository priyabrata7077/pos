from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import *
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r'stock-register', StockRegisterViewSet)
router.register(r'sales-register1', SalesRegister1ViewSet, basename='sales-register1')  # Specify the basename here
router.register(r'customer', CustomerViewSet)
router.register(r'item', ItemViewSet)
router.register(r'sales-pending', SalesPendingViewSet)
router.register(r'transaction-details', TransactionDetailsViewSet)
router.register(r'purchasedetails', PurchaseDetailsViewSet)
router.register(r'purchaseregister', PurchaseRegisterViewSet)
router.register(r'purchase-pending', PurchasePendingViewSet)
router.register(r'accountsmaster', AccountsMasterViewSet)
router.register(r'employee', EmployeeViewSet)

router.register(r'businesses', BusinessViewSet)
urlpatterns = [
    #path('items/', api_view_items, name='api-items'),
    path('current_user/', current_user, name='current_user'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('business/', BusinessListCreateView.as_view(), name='business-list-create'),
    path('business/<int:pk>/', BusinessDetailView.as_view(), name='business-detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('business/<str:owner>/', BusinessDetailView.as_view(), name='business-detail'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', HomeView.as_view(), name ='home'),
    path('logout/', LogoutView.as_view(), name ='logout'),
    path('', include(router.urls)),
    path('get-item-name/<int:item_id>/', get_item_name, name='get_item_name'),
    path('token/', login, name='login'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('units/', UnitListView.as_view(), name='unit-list'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/',TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
]
urlpatterns += router.urls