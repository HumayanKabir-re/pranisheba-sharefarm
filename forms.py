from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import get_user_model, password_validation
from django import forms
from django.shortcuts import get_object_or_404, redirect
from requests import request
from .models import UserProfile, InvestorNomineeDetails, InvestorBankingDetails
from bootstrap_modal_forms.forms import BSModalModelForm
import unicodedata
from django.template import loader
from django.utils.translation import gettext, gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.models import User


from django import forms #NEW, for customizing Form to have Calender  - 16/03/2022

User = get_user_model()

class DateInput(forms.DateInput):   # NEW, Moved Up to be included in Edit Profile - 30/03/2022
    input_type = 'date'

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = User
        fields = "__all__"


class CustomUserRegisterForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'password1', 'password2', 'is_agreed', 'is_investor']

    def __init__(self, *args, **kwargs):
        super(CustomUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['is_investor'].disabled = True
        self.fields['is_investor'].initial = True


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['phone', 'email', 'password', ]


class ProfileUpdateForm(BSModalModelForm):      # NEW, Added for Edit Profile - 30/03/2022
    class Meta:
        model = UserProfile
        fields = [f.name for f in UserProfile._meta.fields]
        exclude = ('profile_user', 'profile_img')
        widgets = {
            'dob': DateInput(),
        }


class UpdateProfilePictureForm(BSModalModelForm):
   class Meta:
       model = UserProfile
       fields = ['profile_img']
    #    exclude = ('profile_user', 'name', 'company_name', 'occupation', 'nationality', 'nid', 
    #    'dob', 'address1', 'address2', 'zip_code', 'city', 'country',)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    error_messages = {
        'invalid_email': _(
            "Email address does not exist! "
        ),
        'inactive': _("This account is inactive."),
    }

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
               _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def clean(self):
        # test the rate limit by passing in the cached user object
        # clean_data = self.cleaned_data
        email = self.cleaned_data.get("email")
        email_field_name = User.get_email_field_name()
        user = User._default_manager.filter(**{
            '%s__iexact' % email_field_name: email
        })
        if email is not None:

            if not user:
                raise self.get_invalid_email_error()
            else:
                self.is_active_user(user)

        return self.cleaned_data

    def get_invalid_email_error(self):
        return ValidationError(
            self.error_messages['invalid_email'],
            code='invalid_email',
            # params={'username': self.username_field.verbose_name},
        )

    def is_active_user(self, users):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        for user in users:
            if not user.is_active:
                raise ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]

        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = User.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )


class SetPasswordForm(forms.Form):      #used to change or reset password
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(forms.Form):       #used to change or reset password
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'incorrect_password': _('The entered password is incorrect.'),
        'old_password': _('Your triying the old password.')
    }
    current_password = forms.CharField(
        label=_("Current password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password2(self):
        password0 = self.cleaned_data.get('current_password')
        
        # current Password check block
        
        #   # user = authenticate(request=self.context.get('request'), password=current_password)
        user = self.request.user
        
        isCorrectPassword = self.request.user.check_password(password0)
        
        if (isCorrectPassword == False):
            raise ValidationError(
                self.error_messages['incorrect_password'],
                code='incorrect_password',
            )
        
        # return password2
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        password0 = self.cleaned_data.get('current_password')
        
        # current Password check block
        
        #   # user = authenticate(request=self.context.get('request'), password=current_password)
        user = self.request.user
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if (password0 == password1) or (password0 == password2):
                raise ValidationError(
                    self.error_messages['old_password'],
                    code='old_password',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password2"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
    

class MultipleForm(forms.Form):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class ModelMultipleForm(forms.ModelForm):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class ContactForm(MultipleForm):
    title = forms.CharField(max_length=150)
    message = forms.CharField(max_length=200, widget=forms.TextInput)


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [f.name for f in UserProfile._meta.fields]
        exclude = ('profile_user',) # NEW, Removed 'profile_img' to handle files - 16/03/2022
        widgets = {
            'dob': DateInput(),     # NEW, Added for Calender - 16/03/2022
        }


class BankInfoForm(forms.ModelForm):
    class Meta:
        model = InvestorBankingDetails
        fields = [f.name for f in InvestorBankingDetails._meta.fields]
        exclude = ('investor',)


class NomineeInfoForm(forms.ModelForm):
    class Meta:
        model = InvestorNomineeDetails
        fields = [f.name for f in InvestorNomineeDetails._meta.fields]
        exclude = ('investor',)
