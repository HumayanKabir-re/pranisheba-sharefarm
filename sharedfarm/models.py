import datetime
import calendar
from django.db import models
from django.utils.translation import ugettext_lazy as _, ungettext, ugettext_lazy
from django.core.validators import MaxValueValidator, MinValueValidator

from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_apphooks_config.models import AppHookConfig
from parler.models import TranslatableModel, TranslatedFields
from cms.models.pluginmodel import CMSPlugin
from .cms_appconfig import SharedFarmConfig
from aldryn_apphooks_config.managers import AppHookConfigManager
from aldryn_apphooks_config.fields import AppHookConfigField
import uuid
from django.contrib.auth import get_user_model
from .config import PayStatus
from core.models import UserFcmToken

User = get_user_model()


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


# # Create your models here.
#
#
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DivDisThaCommon(models.Model):
    name = models.CharField(max_length=200)
    bn_name = models.CharField(max_length=200, verbose_name='Bangla Name')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.bn_name})"


class Division(DivDisThaCommon):
    pass


class District(DivDisThaCommon):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, name='division')
    lat = models.DecimalField(null=True, decimal_places=7, max_digits=10)
    lon = models.DecimalField(null=True, decimal_places=7, max_digits=10)
    website = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return f"{self.name}"


class Breed(models.Model):
    name = models.CharField(max_length=200, unique=True)
    bn_name = models.CharField(max_length=200, unique=True, verbose_name='Bangla Name')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class CowGenderOptions(models.Model):
    COW_GENDER = (
        ('cow', 'Cow'),
        ('bull', 'Bull'),
        ('heifer', 'Heifer')
    )

    class Meta:
        abstract = True


_FAQ_CATEGORY_CHOICES = (
    ('general', ugettext_lazy('FAQ for General')),
    ('shariah', ugettext_lazy('FAQ for Shariah')),

)


class FundCategory(models.Model):
    GENERAL = 'general'
    SHARIAH = 'shariah'
    TYPE = (
        ('general', 'General'),
        ('shariah', 'Shariah'),
    )

    class Meta:
        abstract = True


class Faq(TimeStampedModel):
    category = models.CharField(max_length=10, default=_FAQ_CATEGORY_CHOICES[0],
                                choices=((None,
                                          ugettext_lazy(
                                              "Select FAQ category")),) + _FAQ_CATEGORY_CHOICES)

    def __str__(self):
        return self.category

    def __unicode__(self):
        return self.category


class FaqItem(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.ForeignKey(Faq, on_delete=models.CASCADE, related_name='faq_category',
                                 verbose_name='Faq Category', null=True)

    def __unicode__(self):
        return self.question


class Product(TimeStampedModel):
    app_config = AppHookConfigField(SharedFarmConfig)
    category = models.CharField(max_length=10, default=FundCategory.GENERAL,
                                choices=((None,
                                          ugettext_lazy(
                                              "Select offering category")),) + FundCategory.TYPE)
    image = models.ImageField(upload_to="fund_opportunities", null=True, blank=True)
    name = models.CharField(max_length=200)
    amount = models.DecimalField('amount', max_digits=64, decimal_places=2)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)],
                                           help_text=" Please enter the scheme duration in months (max:12)")
    profit_percentage = models.DecimalField('return', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(1), MaxValueValidator(100)],
                                            help_text=" Please enter the profit return percentage", null=True,
                                            blank=True)
    # shariah_profit_from = models.DecimalField('shariah_profit_from', max_digits=5, decimal_places=2,
    #                                           validators=[MinValueValidator(1), MaxValueValidator(100)],
    #                                           help_text=" Please enter the probable least profit return percentage ",
    #                                           null=True,
    #                                           blank=True)
    shariah_profit_to = models.DecimalField('shariah_profit_to', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(1), MaxValueValidator(100)],
                                            help_text=" Please enter the probable max profit return percentage ",
                                            null=True,
                                            blank=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, name='breed', verbose_name='Cattle Breed')
    gender = models.CharField(max_length=10, choices=CowGenderOptions.COW_GENDER)
    location = models.ForeignKey(District, models.SET_NULL, blank=False, null=True, name='location')
    average_weight = models.DecimalField('average_weight', max_digits=10, decimal_places=2,
                                         help_text=" Please enter the average weight in kg eg: 110-120 KG")
    source = models.CharField(max_length=200, null=True, blank=True)
    growth_timeline = models.CharField(max_length=200, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    number_of_cows = models.PositiveIntegerField(default=0,
                                                 help_text=" Please enter the total number of available cows")
    faq = models.ForeignKey(Faq, models.SET_NULL, null=True)
    objects = AppHookConfigManager()

    class Meta:
        ordering = ('is_active',)
        verbose_name_plural = 'Funding Opportunities'

    def __unicode__(self):
        return self.name

    def get_offering_display(self):
        # self.get_expired_date()
        if self.category == FundCategory.SHARIAH:
            return f"{self.duration} months contract period with upto {self.shariah_profit_to} % Profit Sharing" #{self.shariah_profit_from}% to

        else:
            return f"{self.duration} months contract period with {self.profit_percentage}% Return on Funding"

        pass

    def get_net_profit(self):
        if self.category == FundCategory.GENERAL:
            return _('%(net_profit).02f BDT') % {'net_profit': ((self.amount * self.profit_percentage) / 100)}
        return None

    def calculate_net_profit(self):
        if self.category == FundCategory.GENERAL:
            return round((self.amount * self.profit_percentage) / 100, 2)
        return None

    def is_cow_available(self):
        return self.number_of_cows > sum(
            [each_invoice.unit for each_invoice in self.invoice_product.filter(is_paid=True)])

    is_cow_available.boolean = True

    def get_available_number_of_cows(self):
        if self.is_cow_available():
            return self.number_of_cows - sum(
                [each_invoice.unit for each_invoice in self.invoice_product.filter(is_paid=True)])
        else:
            return 0

    def calculate_total(self, unit):
        return unit * self.amount

        # def get_absolute_url(self, lang=None):
    #     lang = _get_language(self, lang)
    #     with switch_language(self, lang):
    #         category = self.categories.first()
    #         kwargs = {}
    #         if self.date_published:
    #             current_date = self.date_published
    #         else:
    #             current_date = self.date_created
    #         urlconf = get_setting("PERMALINK_URLS")[self.app_config.url_patterns]
    #         if "<int:year>" in urlconf:
    #             kwargs["year"] = current_date.year
    #         if "<int:month>" in urlconf:
    #             kwargs["month"] = "%02d" % current_date.month
    #         if "<int:day>" in urlconf:
    #             kwargs["day"] = "%02d" % current_date.day
    #         if "<str:slug>" in urlconf or "<slug:slug>" in urlconf:
    #             kwargs["slug"] = self.safe_translation_getter("slug", language_code=lang, any_language=True)  # NOQA
    #         if "<slug:category>" in urlconf or "<str:category>" in urlconf:
    #             kwargs["category"] = category.safe_translation_getter(
    #                 "slug", language_code=lang, any_language=True
    #             )  # NOQA
    #         return reverse(
    #             "%s:post-detail" % self.app_config.namespace, kwargs=kwargs, current_app=self.app_config.namespace
    #         )


class WhatsNewBanner(TimeStampedModel):
    image = models.ImageField(upload_to="whats_new", null=False, blank=False)
    product = models.ForeignKey(Product,
                                null=True, on_delete=models.SET_NULL, blank=True, editable=True,
                                related_name='whats_new_product')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.pk}"


class Subscription(TimeStampedModel):
    email = models.EmailField(help_text='Email address', unique=True)

    def __str__(self):
        return f'{self.email}'


class SubscriptionPluginModel(CMSPlugin):
    title = models.CharField(u'title',
                             blank=True,
                             help_text=u'Optional. Title of the widget.',
                             max_length=64,
                             )


# Create payment models here.


class Payment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=200, null=True, blank=True, unique=True)
    status = models.IntegerField(choices=PayStatus.CHOICES, default=PayStatus.PENDING, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.pk}"


class PaymentLog(TimeStampedModel):
    payment = models.ForeignKey(Payment, models.SET_NULL, blank=True, null=True)
    txID = models.CharField(max_length=200, null=False, blank=True, unique=True)
    bankTxID = models.CharField(max_length=200, null=True, blank=True)
    bankTxStatus = models.CharField(max_length=10, choices=PayStatus.spChoices, null=False, blank=False,
                                    default="CANCEL")
    txnAmount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    spCode = models.CharField(max_length=10, null=True, blank=False)
    spCodeDes = models.CharField(max_length=50, null=True, blank=True)
    paymentOption = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"


class Invoice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=True)
    product = models.ForeignKey(Product,
                                null=True, on_delete=models.SET_NULL, blank=True, editable=True,
                                related_name='invoice_product')
    user = models.ForeignKey(User,
                             null=True, blank=True, on_delete=models.CASCADE, editable=True)
    payment = models.ForeignKey(Payment, models.SET_NULL, null=True, blank=True, name='payment', editable=True)
    amount = models.DecimalField(max_digits=64, decimal_places=2,
                                 null=True, blank=True, editable=True)
    unit = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Invoice, self).save()
        # print(self.product.get_available_number_of_cows())
        if self.is_paid and self.product.get_available_number_of_cows() == 0:
            self.product.is_active = False
            self.product.save()
            # print(self.product.is_active)
        if self.is_paid and 0 < self.product.get_available_number_of_cows() <= self.product.number_of_cows:
            self.product.is_active = True
            self.product.save()

    def get_farm_mature_date(self):
        return add_months(self.timestamp, self.product.duration)

    class Meta:
        ordering = ('-timestamp',)


def cow_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'cow-image/{0}/{1}'.format(instance.cow_id, filename)


class HmsCattle(TimeStampedModel):
    cow_id = models.IntegerField(null=False, blank=False)
    cow_name = models.CharField(max_length=200, null=False, blank=False)
    ear_tag = models.CharField(max_length=200, verbose_name='Cow Id/ Ear Tag', help_text='Any identification number',
                               null=False, blank=False)
    cow_type = models.ForeignKey(Breed, models.SET_NULL, name='cow_type', verbose_name='Cow Type', null=True)
    image = models.ImageField(upload_to=cow_image_directory_path)
    farm_id = models.IntegerField(null=False, blank=False)
    farm_name = models.CharField(max_length=200)
    farm_no = models.CharField(max_length=100, blank=False, null=False)
    status = models.BooleanField(default=False)

    def get_farm_name(self):
        return _('%(farm_name)(%(farm_no))') % {'farm_name': self.farm_name, 'farm_no': self.farm_no}

    def __str__(self):
        return f"{self.cow_id}"


from djangocms_text_ckeditor.fields import HTMLField
from djangocms_text_ckeditor.models import AbstractText, CMSPlugin as ck_CMSPlugin


class MyModel(AbstractText):
    myfield = HTMLField(null=True, blank=True, configuration="BLOG_POST_TEXT_CKEDITOR")


class HowWeWorkHead(ck_CMSPlugin):
    myfield = HTMLField(null=True, blank=True, configuration="BLOG_POST_TEXT_CKEDITOR")
    number_of_steps = models.CharField(max_length=10, null=True, blank=True)


class HowWeWorkStepItem(CMSPlugin):
    step_no = models.PositiveIntegerField(null=True, blank=True, )
    step_head = models.CharField(max_length=200, null=True, blank=True)
    step_details = models.TextField()

    def __str__(self):
        return f"{self.step_no}"


from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import fcm_notify
import json


#@receiver(post_save, sender=Product)
def new_product_fcm_signal(sender, instance, created, **kwargs):
    if created:
        all_list = UserFcmToken.objects.all().values_list('fcm_token', flat=True)
        receiver_list = list(all_list)
        data_message = {
            "id": instance.id,
            "name": instance.name,
            "category": instance.category,
            "duration": instance.duration,
            "amount": instance.amount
        }
        fcm_notify.apply_async(
            args=(receiver_list, data_message),
            countdown=1, expires=10
        )  # task will be executed after 'storing the event data'
