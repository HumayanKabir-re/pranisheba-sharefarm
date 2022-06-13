from django.contrib import admin
from django.utils.translation import ugettext as _, ungettext, ugettext_lazy
from .models import *
from .forms import DropdownModelForm
from aldryn_apphooks_config.admin import ModelAppHookConfig, BaseAppHookConfig


# Register your models here.

def _return(prod):
    return prod.get_offering_display()


class FaqItemAdminStackedInline(admin.StackedInline):
    model = FaqItem
    extra = 0
    fields = ('question', 'answer', 'category')


class FaqAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Faq._meta.fields]
    inlines = [FaqItemAdminStackedInline]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Subscription._meta.fields]


class HmsCattleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in HmsCattle._meta.fields]


class WhatsNewBannerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WhatsNewBanner._meta.fields]


admin.site.register(Faq, FaqAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(HmsCattle, HmsCattleAdmin)
admin.site.register(WhatsNewBanner, WhatsNewBannerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', _return, 'is_active', 'location', 'app_config')
    list_select_related = ('location',)
    # list_filter = (
    #     'app_config',
    # )
    fieldsets = (
        (_('App Config'), {'fields': ('app_config',)}),
        (_('Offering Type'), {'fields': ('category',)}),
        (_('Basic Info'), {'fields': ('image', 'name', 'amount', 'location', 'duration', 'breed', 'gender')}),
        ('Profit Return', {
            'fields': ('profit_percentage',),
            'classes': ('general_css',)
        }),
        (_('Shariah Profit Sharing'), {
            'fields': ('shariah_profit_to',), #'shariah_profit_from', 
            'classes': ('shariah_css',)
        }),
        (_('More Information'), {
            'fields': ('average_weight', 'source', 'growth_timeline', 'details', 'number_of_cows', 'faq'),
            'classes': ('more_css',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        })

    )

    form = DropdownModelForm

    class Media:
        js = ('js/category_admin.js',)


admin.site.register(Product, ProductAdmin)


class SharedFarmConfigAdmin(BaseAppHookConfig, admin.ModelAdmin):
    def get_config_fields(self):
        return (
            'paginate_by',
            'config.title',
        )


admin.site.register(SharedFarmConfig, SharedFarmConfigAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Invoice._meta.fields]


class PaymentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Payment._meta.fields]

    # def get_readonly_fields(self, request, obj=None):
    #     return self.fields or [f.name for f in self.model._meta.fields]
    #
    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return (request.method in ['GET', 'HEAD'] and
    #             super().has_change_permission(request, obj))
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
