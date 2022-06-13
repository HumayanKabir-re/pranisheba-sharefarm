from itertools import product
from MySQLdb import Timestamp
from django.contrib import admin
from sharedfarm.models import Invoice, Product
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUerAdmin
from django.contrib.auth.models import Group
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import ugettext_lazy as _


# # Define a new User admin
# class UserFcmTokenInline(admin.TabularInline):
#     model = UserFcmToken
class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserBankInline(admin.StackedInline):
    model = InvestorBankingDetails


class UserNomineeInline(admin.StackedInline): 
    model = InvestorNomineeDetails


# class ProductListInline(admin.TabularInline):
#     model = Product
    

class InvoiceListInline(admin.StackedInline):   # was admin.TabularInline
    model = Invoice
    extra = 0   # Delete the 3 default extra values
    # readonly_fields: Invoice['timestamp', 'investor_product', 'payment', 'amount', 'unit', ]
    # Move the above file to a new class, video 4:34

class SettingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Setting._meta.fields]
    

class UserAdmin(BaseUerAdmin):
    # list_display = ('phone', 'email',  'name', 'is_active', 'is_viewer')
    # list_filter = ('is_viewer', 'is_active', 'is_superuser')
    # fieldsets = (
    #     *BaseUserAdmin.fieldsets,  # original form fieldsets, expanded
    #     (  # new fieldset added on to the bottom
    #         'Viewer status',  # group heading of your choice; set to None for a blank space instead of a header
    #         {
    #             'fields': (
    #                 'is_viewer', 'is_agreed', 'is_subscribed'
    #             ),
    #         },
    #     ),
    # )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('phone',)}),
        (_('Permissions'), {'fields': ('is_investor', 'is_active', 'is_staff', 'is_superuser', 'is_agreed')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'phone', 'is_staff', 'is_active',)
    # list_filter = ['user_type']
    inlines = (UserProfileInline, UserBankInline, UserNomineeInline, InvoiceListInline, ) #ProductListInline,
    search_fields = ('email', 'phone',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    # exclude = ('username', )


class UserFCMTokenAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserFcmToken._meta.fields]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(UserFcmToken, UserFCMTokenAdmin)
# admin.site.unregister(Group)

# admin.site.register(Invoice)
# admin.site.register(Product)