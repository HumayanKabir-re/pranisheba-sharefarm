# -*- coding: utf-8 -*-
from django.conf.urls import url, re_path, include
from django.urls import path
from . import views
from rest_framework import routers

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
]

urlpatterns = [
    url('^login/$', views.CustomLoginView.as_view(), name='login'),
    url('^signup/', views.SignUpView.as_view(), name='signup'),
    url('^profile/$', views.user_profile, name='profile'),
    url('^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url('^my_farms/$', views.MyFarms.as_view(), name='my_farms'),
    url(r"^read_farm/(?P<pk>\d+)/$", views.FarmDetailsView.as_view(), name='read_farm'),
    # url('^edit_profile', views.AccountProfilesView.as_view(), name='edit_profile'),
    url(r"^profile/(?P<pk>\d+)/$",
        views.AccountProfilesView.as_view(),
        name='edit_profile'
        ),
    url("^logout/$", views.user_logout, name='logout')
    # {'next_page': '/'}


]
