from rest_framework import serializers
import json
from django.db.models import Q
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import UserProfile, UserOtp, InvestorBankingDetails, InvestorNomineeDetails, UserFcmToken

import pyotp
from .config import UserOtpConfig

# from .models import UserOtp, UserFcmToken
# from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()


# class UserDeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserFcmToken
#         fields = ('id', 'fcm_token', 'details', 'created', 'modified', 'is_owner')
class CustomeAuthTokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(label=_("Token"), help_text="Time based token")
    expires_in = serializers.CharField(label=_("Expires In"), help_text="Second left to expire the given token")
    username = serializers.CharField(label=_("Username"), help_text="User name for the token.")


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    fcm_token = serializers.CharField(required=True, label=_("FCM Token"), help_text="fcm token for cloud messages")

    # details = serializers.CharField(required=False, label=_("Details"), help_text="any extra info about the device")

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        fcm_token = attrs.get('fcm_token')
        # details = attrs.get('details')
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                email_or_phone=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            # fcm_user check
            UserFcmToken.objects.filter(fcm_token=fcm_token).delete()
            UserFcmToken.objects.update_or_create(fcm_token=fcm_token,
                                                  defaults={'user': user})

        else:
            msg = _('Must include "username", "password", "fcm_token".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        attrs['fcm_token'] = fcm_token
        # attrs['details'] = details
        return attrs


# Reset-password Serializer
class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))

    def validate(self, attrs):
        username = attrs.get('username')

        if username:
            try:
                user = User.objects.get(
                    Q(email=username) | Q(phone=username)
                )

            except Exception as e:

                msg = _('Unable to process with provided credentials.')
                raise serializers.ValidationError(msg, code='invalid')

        else:
            msg = _('Must include "username/mobile no."')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


# ForgotPasswordConfirm serializer
class ResetPasswordConfirmSerializer(serializers.Serializer):
    otp = serializers.CharField(label=_("otp"))
    new_password = serializers.CharField(label=_("new_password"),
                                         style={'input_type': 'password'},
                                         trim_whitespace=False)

    def validate(self, attrs):
        otp = attrs.get('otp')
        new_password = attrs.get('new_password')

        if otp and new_password:
            try:
                user = User.objects.filter(id__in=[user.user_id for user in UserOtp.objects.filter(otp=otp)]).get()
            except Exception as e:
                msg = _('Unable to process with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            totp = pyotp.TOTP('base32secret3232', digits=4)
            valid_window = UserOtpConfig.VALID_WINDOW
            if totp.verify(otp, valid_window=int(valid_window)) is False:
                msg = _('Wrong OTP or OTP time expired')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['otp'] = otp
        attrs['new_password'] = new_password
        attrs['user'] = user
        return attrs


class UserSignUpSerializer(serializers.Serializer):
    phone = serializers.CharField(label=_("phone"), required=True)
    email = serializers.EmailField(label=_("email"), required=False)
    is_investor = serializers.BooleanField(label=_("is_investor"), required=True)
    is_agreed = serializers.BooleanField(label=_("is_agreed"), required=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def check_if_exist(self, username, password):
        user = authenticate(request=self.context.get('request'),
                            email_or_phone=username, password=password)
        if user:
            msg = _(f'User is already registered with this {username}')
            raise serializers.ValidationError(msg, code='authorization')

    def validate(self, attrs):
        phone = attrs.get('phone')
        # name = attrs.get('name')
        email = attrs.get('email')
        password = attrs.get('password')
        is_investor = attrs.get('is_investor')
        is_agreed = attrs.get('is_agreed')
        # print(email)
        is_email = False
        is_phone = False
        if phone:
            self.check_if_exist(phone, password)
            pass
        if email:
            self.check_if_exist(email, password)
            pass

        if phone and password or email:
            if email is not None:

                newuser, created = User.objects.update_or_create(
                    phone=phone,
                    defaults={'email': email, 'is_investor': is_investor, 'is_agreed': is_agreed},

                )
                pass
            else:
                newuser, created = User.objects.update_or_create(
                    phone=phone,
                    defaults={'is_investor': is_investor, 'is_agreed': is_agreed},

                )
                # print(created)
            newuser.set_password(password)
            newuser.save()
            user = newuser
            pass
        else:
            msg = _(
                'Must include "phone", "password", "is_agreed", "is_investor".')
            raise serializers.ValidationError(msg, code='authorization')
            pass

        # attrs['user'] = user
        # attrs['password'] = password
        return attrs

    def create(self, validated_data):
        return User(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='profile',)

    class Meta:
        model = UserProfile
        # fields = ['id', 'name', 'profile_img', 'nid', 'dob', 'address1', 'address2', 'zip_code', 'city', 'country']
        exclude = ['profile_user', ]


class ProfileAddEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['profile_user', ]


class InvestorBankingDetailsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorBankingDetails
        exclude = ('investor',)


class InvestorNomineeDetailsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorNomineeDetails
        exclude = ('investor',)


class InvestorInformationSerializer(serializers.Serializer):
    profile = ProfileSerializer(many=True)
    bank_info = InvestorBankingDetailsProfileSerializer(many=True)
    nominee_info = InvestorNomineeDetailsProfileSerializer(many=True)

