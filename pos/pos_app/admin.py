from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(StockRegister)
class StockRegisterAdmin(admin.ModelAdmin):
    ist_display = ('osid', 'get_item_name', 'itemqty', 'purrate', 'itemmrp', 'itemsalerate', 'itembarcode', 'locid')


    def get_item_name(self, obj):
        return obj.itemid.itemname if obj.itemid else "N/A"
    
    get_item_name.short_description = 'Item Name'
admin.site.register(SalesRegister1)
admin.site.register(customers)
admin.site.register(Item)
admin.site.register(SalesPending)
admin.site.register(transaction_details)
admin.site.register(Transaction)
admin.site.register(AccountsMaster1)
admin.site.register(PurchaseRegister1)
admin.site.register(purchasedetails1)
admin.site.register(EmployeeMaster)
admin.site.register(PurchasePending)
admin.site.register(business)
admin.site.register(Owner)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Attribute_options)
admin.site.register(Attribute)
admin.site.register(Company)
admin.site.register(Unit)