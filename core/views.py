from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView, BSModalUpdateView, BSModalReadView, \
    BSModalFormView
from .forms import CustomAuthenticationForm, CustomUserRegisterForm, UserUpdateForm, ProfileUpdateForm, \
    PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model, logout, login
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserProfile, UserOtp, InvestorBankingDetails, InvestorNomineeDetails, UserFcmToken
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.schemas import ManualSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .util import *
import pyotp
from .config import UserOtpConfig
from aps_shared_farm.sms import ShurjoBartaSMS
from aps_shared_farm.tasks import signup_success_email, password_reset_email
from sharedfarm.views import get_user_invest_summery
from sharedfarm.models import Invoice
from rest_framework.decorators import api_view, permission_classes
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


# Create your views here.
class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'core/login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('core:profile'))


class SignUpView(BSModalCreateView):
    form_class = CustomUserRegisterForm
    template_name = 'core/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('core:login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        url = "https://" + self.request.get_host() + str(self.success_url)
        signup_success_email(self.object.phone, self.object.email, url)

        return super().form_valid(form)


@login_required
def user_logout(request):
    try:
        logout(request)
    except:
        pass

    return redirect('sharedfarm:index')


@login_required
def user_profile(request):
    # if request.method == "POST":
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('core:profile')
    # # user_id = int(user_id)
    # # try:
    # #     user_sel = User.objects.get(id=request.user.id)
    # # except User.DoesNotExist:
    # #     return redirect('sharedfarm:index')
    # # u_form = UserUpdateForm(request.POST or None, instance=user_sel)
    # # p_form = ProfileUpdateForm(request.POST or None, instance=user_sel)
    # # if profile_form.is_valid():
    # #     profile_form.save()
    #
    # #         messages.success(request, f'updated successfully')
    # #         return redirect('core:login')
    # else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'invest_summery': get_user_invest_summery(request.user)
    }

    return render(request, 'core/profile.html', context)


class MyFarms(generic.ListView):
    model = Invoice
    context_object_name = 'invoices'
    template_name = 'core/invoice.html'

    def get_context_data(self, **kwargs):
        context = super(MyFarms, self).get_context_data(**kwargs)
        context.update({
            'invest_summery': get_user_invest_summery(self.request.user),
        })
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        # if 'type' in self.request.GET:
        #     qs = qs.filter(book_type=int(self.request.GET['type']))
        return qs.filter(is_paid=True).filter(user=self.request.user)


class FarmDetailsView(BSModalReadView):
    model = Invoice
    template_name = 'core/farm_details.html'


class AccountProfilesView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    # When I ask for user with Student Profile
    model = UserProfile
    form_class = ProfileUpdateForm

    success_message = 'Success: Profile Updated successfully!'

    success_url = reverse_lazy('core:profile')
    template_name = 'core/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super(AccountProfilesView, self).get_context_data(**kwargs)
        user = self.request.user
        if not self.request.POST:
            if user:
                context['p_form'] = ProfileUpdateForm(instance=self.request.user.userprofile)

        else:
            if user:
                context['p_form'] = ProfileUpdateForm(self.request.POST, self.request.FILES,
                                                      instance=self.request.user.userprofile)
        '''
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET,
                instance=user)
        '''
        profile = user.get_user_profile()
        context.update({'userprofile': profile})
        # if user.is_student:
        #     profile = user.get_student_profile()
        #     context.update({'userprofile': profile})
        # elif user.is_professor:
        #     profile = user.get_professor_profile()
        #     context.update({'userprofile': profile})
        # elif user.is_executive:
        #     profile = user.get_executive_profile()
        #     context.update({'userprofile': profile})
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        user = self.request.user
        # user = form.save()
        if user:
            profile = context['p_form'].save(commit=False)
            profile.profile_user = user
            profile.save()
        # elif user.is_professor:
        #     professor = context['form_professor'].save(commit=False)
        #     professor.user = user
        #     professor.save()
        # elif user.is_executive:
        #     executive = context['form_executive'].save(commit=False)
        #     executive.user = user
        #     executive.save()
        # elif user.is_student and user.is_professor and user.is_executive:
        #     student = context['form_student'].save(commit=False)
        #     student.user = user
        #     student.save()
        #     professor = context['form_professor'].save(commit=False)
        #     professor.user = user
        #     professor.save()
        #     executive = context['form_executive'].save(commit=False)
        #     executive.user = user
        #     executive.save()

        return super(AccountProfilesView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                name="username",
                required=True,
                location='form',
                schema=coreschema.String(
                    title="Username",
                    description="Valid username for authentication",
                ),
            ),
            coreapi.Field(
                name="password",
                required=True,
                location='form',
                schema=coreschema.String(
                    title="Password",
                    description="Valid password for authentication",
                ),
            ),
            coreapi.Field(
                name="fcm_token",
                required=True,
                location='form',
                schema=coreschema.String(
                    title="FCM Token",
                    description="FCM token for cloud messaging",
                ),
            ),

        ],
        encoding="application/json",
    )
    post_response = openapi.Response('Token response description', CustomeAuthTokenResponseSerializer)

    @swagger_auto_schema(responses={201: post_response})
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data,
                                               context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        fcm_token = serializer.validated_data['fcm_token']
        # details = serializer.validated_data['details']
        token, created = Token.objects.get_or_create(user=user)
        # count_device = UserDeviceSerializer(UserFcmToken.objects.filter(user=user), many=True,
        #                                     context={'request': request})

        is_expired, token = token_expire_handler(token)

        return Response({
            'token': token.key,
            'expires_in': expires_in(token),
            'username': user.get_email_or_phone(),

        })


class SignUpRestView(CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        base_url = request.get_host()
        login_endpoint = reverse_lazy('core:login')
        self.perform_create(serializer)
        login_url = "https://" + base_url + str(login_endpoint)

        if serializer.data['email']:
            signup_success_email(serializer.data['phone'], serializer.data['email'], login_url)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data['phone'],
            'details': 'User successfully registered to the Adrosho Pranisheba JouthoKhamar'
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class ProfileRestViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(profile_user=self.request.user.pk)

    # @swagger_auto_schema(auto_schema=None)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(request.data)
        serializer = ProfileAddEditSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# API END POINTS VIEW SETS
class InvestorCreateUpdateViewSet:
    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)

    def perform_update(self, serializer):
        serializer.save(investor=self.request.user)


class BankDetailsViewSet(InvestorCreateUpdateViewSet, viewsets.ModelViewSet):
    queryset = InvestorBankingDetails.objects.all()
    serializer_class = InvestorBankingDetailsProfileSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestorBankingDetails.objects.filter(investor=self.request.user.pk)


class NomineeDetailsViewSet(InvestorCreateUpdateViewSet, viewsets.ModelViewSet):
    queryset = InvestorNomineeDetails.objects.all()
    serializer_class = InvestorNomineeDetailsProfileSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestorNomineeDetails.objects.filter(investor=self.request.user.pk)


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def send_code(self):
        totp = pyotp.TOTP('base32secret3232', digits=4)
        otp = totp.now()
        UserOtp.objects.update_or_create(user=self.user, defaults={'otp': otp})
        if self.user.email:
            password_reset_email(self.user, otp, UserOtpConfig.VALID_WINDOW)
        else:
            message = f'Use OTP: {otp} to reset password for jouthoKhamar user account. ' \
                      f'This OTP will be valid for {UserOtpConfig.VALID_WINDOW} seconds.'
            user_sms = ShurjoBartaSMS(destination=self.user.phone, message=message)
            response = user_sms.send()
            print(response)
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.user = serializer.validated_data['user']
        self.send_code()

        return Response({
            'user': self.user.get_email_or_phone(),
            'details': 'an OTP sent to requested USER NO or email.',
            'email': self.user.email if self.user.email else None
        })


class ResetPasswordConfirmView(CreateAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        user = serializer.validated_data['user']

        user.set_password(new_password)
        user.save()
        return Response({
            'message': f'Password successfully changed for this user id: {user.get_email_or_phone()}'
        })


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'emails/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'core/txt/password_reset_subject.txt'
    success_url = reverse_lazy('core:password_reset_done')
    template_name = 'core/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'core/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('core:password_reset_complete')
    template_name = 'core/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'core/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context
