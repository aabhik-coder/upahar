from django.contrib import admin
from .models import Category,Customer,Product ,Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)


class OrdersAdmin(admin.ModelAdmin):
    list_display =('customer', 'product', 'date','order_status')
    # readonly_fields =  ('user', 'paid', 'amount','number_of_people', 'package')
    # def has_add_permission(self, request):
    #     return False
    
    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        # Customize the update permission logic here
        # For example, you can allow update only if the user is staff
        return request.user.is_superuser

admin.site.register(Order,OrdersAdmin)