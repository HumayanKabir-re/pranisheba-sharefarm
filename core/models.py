from django.db import models

# Create your models here.

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


# Create your models here.
class Setting(models.Model):
    option_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    option_value = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.option_name)
        super(Setting, self).save(*args, **kwargs)

    def __str__(self):
        return self.option_name


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex="[^1-9][1][0-9]{9,9}\\b",
                                 message="Phone number must be entered in the format: '01912345678'."
                                         " Up to 11 digits allowed.", )
    phone = models.CharField(validators=[phone_regex], max_length=13, null=True, help_text='Contact phone number',
                             unique=True)
    email = models.EmailField(null=True, help_text='Email address', )
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))

    is_investor = models.BooleanField('investor status', default=False,
                                      help_text=_('Designates whether the user is investor or not'))
    is_agreed = models.BooleanField('terms & conditions', default=True,
                                    help_text=_('Designates whether the user accepts RBS terms and conditions'))
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_email_or_phone()

    def get_email_or_phone(self):
        if self.phone is None:
            return self.email
        else:
            return self.phone

    def get_user_profile(self):
        user_profile = None
        if hasattr(self, 'userprofile'):
            student_profile = self.userprofile
        return user_profile


class UserOtp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class UserFcmToken(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    fcm_token = models.CharField(max_length=400)

    def __str__(self):
        return self.fcm_token


class UserProfile(models.Model):
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default="profile_user/profile_img.jpg", upload_to="profile_user")
    name = models.CharField(_('Full Name'), help_text=" Please enter the Full Name according to NID",
                            max_length=30, blank=True)

    company_name = models.CharField(_('Company Name'),
                                    help_text=" Please enter the Investor Organization/ Company Name.",
                                    max_length=100, blank=True, null=True)
    occupation = models.CharField(_('Occupation/Business Type'),
                                  help_text=" Please enter the Investor Occupation/Business Type.",
                                  max_length=255, blank=True, null=True)
    nationality = models.CharField(_("Nationality"), max_length=30, blank=True, null=True)
    nid = models.CharField(_("National ID"), max_length=17, blank=True, null=True)
    dob = models.DateField("Date of Birth", null=True, blank=True)
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
        null=True
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        null=True
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
        null=True
    )

    city = models.CharField(
        "City",
        max_length=1024,
        null=True
    )

    country = models.CharField(
        "Country",
        max_length=1024,
        null=True
    )


class InvestorBankingDetails(models.Model):
    investor = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_('Bank Name'), help_text=" Please enter the Bank Name",
                            max_length=100, blank=False, null=False)

    branch_name = models.CharField(_('Bank Branch Name'),
                                   help_text=" Please enter the Bank Branch Name.",
                                   max_length=100, blank=False, null=False)
    account_no = models.CharField(_('Bank Account Number'),
                                  help_text=" Please enter the Bank Account Number",
                                  max_length=100, blank=False, null=False)
    Account_name = models.CharField(_("Account Name"), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.account_no


class InvestorNomineeDetails(models.Model):
    investor = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_('Nominee Name'), help_text=" Please enter the Nominee Name",
                            max_length=100, blank=False, null=False)

    relationship = models.CharField(_('Relationship with Nominee'),
                                    help_text=" Relationship with Nominee.",
                                    max_length=255, blank=False, null=False)
    contact_no = models.CharField(validators=[User.phone_regex], max_length=13, null=False,
                                  help_text='Nominee Contact number',
                                  )
    nid = models.CharField(_("National ID"), max_length=17, blank=False, null=False)

    def __str__(self):
        return self.nid


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(profile_user=instance)
    instance.userprofile.save()
