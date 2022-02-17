from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUerAdmin
from django.contrib.auth.models import Group
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import ugettext_lazy as _


# # Define a new User admin
# class UserFcmTokenInline(admin.TabularInline):
#     model = UserFcmToken

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
    # inlines = (UserFcmTokenInline,)
    search_fields = ('email', 'phone',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    # exclude = ('username', )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Setting, SettingAdmin)
# admin.site.unregister(Group)
