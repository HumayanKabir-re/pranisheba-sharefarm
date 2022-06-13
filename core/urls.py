from re import template
from django.conf.urls import url, re_path, include
from django.urls import path
from . import views
from rest_framework import routers
from .forms import PersonalInfoForm, BankInfoForm, NomineeInfoForm
from django.contrib.auth import views as auth_views
router = routers.DefaultRouter()
app_name = "core"
router.register(r'profile', views.ProfileRestViewSet)
router.register(r'bank', views.BankDetailsViewSet)
router.register(r'nominee', views.NomineeDetailsViewSet)
core_auth_urlpatterns = [

    url(r'^signup/$', views.SignUpRestView.as_view(), name='user-signup'),
    url(r'^api-token-auth/$', views.CustomAuthToken.as_view(), name='api-token-auth'),
    path('', include(router.urls)),
    url(r'^forgot-password/$', views.ResetPasswordView.as_view(), name='forgot-password'),
    url(r'^confirm-password/$', views.ResetPasswordConfirmView.as_view(), name='confirm-password'),
    url(r"^investor_info/$", views.InvestorInformationViewSet.as_view(), name='investor_info'),
]

urlpatterns = [
    url('^login/$', views.CustomLoginView.as_view(), name='login'),
    url('^signup/', views.SignUpView.as_view(), name='signup'),
    url('^profile/$', views.user_profile, name='profile'),
    url('^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_complete/', views.PasswordChangeConfirmView.as_view(), name='password_change_complete'),
    # url(r"^password_change/(?P<pk>\d+)/$", views.PasswordChangeView.as_view(), name='password_change'),
    # url(r"^password_change_complete/$", views.PasswordChangeConfirmView.as_view(), name='password_change_complete'),
    url('^my_farms/$', views.MyFarms.as_view(), name='my_farms'),
    url(r"^read_farm/(?P<pk>\d+)/$", views.FarmDetailsView.as_view(), name='read_farm'),
    #url(r"^investor_form/(?P<product_id>\d+)/$", views.ContactWizard.as_view(), name='investor_form'),
    url(r"^profile/(?P<pk>\d+)/$", views.AccountProfilesView.as_view(), name='profile'), # profile Editing End Point
    url(r"^profile-picture/(?P<pk>\d+)/$", views.AccountProfilesPictureView.as_view(), name='profile-picture'), # profile Editing End Point
    url("^logout/$", views.user_logout, name='logout'),

]
