from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Product, Breed, FundCategory, Subscription, Payment, Invoice
from aldryn_apphooks_config.mixins import AppConfigMixin
from django.urls import reverse_lazy
from .forms import BookModelForm, SubscriptionForm, CheckOutForm, CheckOutConfirmationForm
from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.messages.views import SuccessMessageMixin
from .shurjoPay import ShurjoPay
from .config import *
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from cms.models.pagemodel import Page
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.utils import timezone, dateformat
from django.contrib import messages
# rest_framework modules

from rest_framework.generics import (ListCreateAPIView, DestroyAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     GenericAPIView, ListAPIView)
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
from .filters import *
from rest_framework.reverse import reverse as rest_reverse
from rest_framework import viewsets, status
import xmltodict, json, ast
from rest_framework.permissions import AllowAny, IsAuthenticated
from django import template
from rest_framework.decorators import api_view
from aps_shared_farm.tasks import order_payment_success_email, unit_book_order_payment_email
from django.views.generic.base import TemplateView

register = template.Library()


# Create your views here.

class IndexView(AppConfigMixin, generic.ListView):
    model = Product
    template_name = 'sharedfarm/index.html'
    context_object_name = 'latest_funding_opportunities'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.namespace(self.namespace)

    def get_paginate_by(self, queryset):
        try:
            return self.config.paginate_by
        except AttributeError:
            return 10

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context["general_farm_list"] = self.get_queryset().filter(category=FundCategory.GENERAL)
        context["shariah_farm_list"] = self.get_queryset().filter(category=FundCategory.SHARIAH)

        return context

    @register.filter
    def filter_cat(self, cat):
        result = self.get_queryset().filter(category=cat).count()
        return result


class ContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


# class ProductDetailView(AppConfigMixin, generic.DetailView):
#     context_object_name = "product"
#     base_template_name = "product_detail.html"
#     model = Product
#
#     def get_queryset(self):
#         queryset = self.model._default_manager.all()
#         if not getattr(self.request, "toolbar", None) or not self.request.toolbar.edit_mode_active:
#             # queryset = queryset.published()
#             pass
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#         context['msg'] = 'test'
#         return context
#
#     def get(self, *args, **kwargs):
#         # submit object to cms to get corrent language switcher and selected category behavior
#         if hasattr(self.request, "toolbar"):
#             self.request.toolbar.set_object(self.get_object())
#         return super().get(*args, **kwargs)
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context["meta"] = self.get_object().as_meta()
#     #     context["instant_article"] = self.instant_article
#     #     context["use_placeholder"] = get_setting("USE_PLACEHOLDER")
#     #     setattr(self.request, get_setting("CURRENT_POST_IDENTIFIER"), self.get_object())
#     #     return context
#

from formtools.wizard.views import SessionWizardView, NamedUrlWizardView
from formtools.wizard.forms import ManagementForm
from django.utils.decorators import method_decorator
from core.forms import PersonalInfoForm, BankInfoForm, NomineeInfoForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from collections import OrderedDict
from core.models import InvestorNomineeDetails, InvestorBankingDetails, UserProfile
from django.forms.models import construct_instance

#NEW Added for adding profile image - 14-03-2022
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

TEMPLATES = {
    "checkout": "sharedfarm/product_detail.html",
    "profile": "core/checkout_proceed_form.html",
    "bank": "core/checkout_proceed_form.html",
    "nominee": "core/checkout_proceed_form.html",
    "confirmation": "core/checkout_confirmation.html"
}


class ProductDetailView(SessionWizardView):
    form_list = [("checkout", CheckOutForm), ("profile", PersonalInfoForm), ("bank", BankInfoForm),
                 ("nominee", NomineeInfoForm), ("confirmation", CheckOutConfirmationForm)]
    
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profile_user')) #NEW, added for handling files - 14-03-2022

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.product = Product.objects.get(id=self.kwargs['pk'])
        return super(ProductDetailView, self).dispatch(*args, **kwargs)

    def done(self, form_list, **kwargs):
        profile_instance = UserProfile.objects.get(profile_user=self.request.user)
        bank_instance = InvestorBankingDetails()
        nominee_instance = InvestorNomineeDetails()
        p_data = {}
        b_data = {}
        n_data = {}
        c_data = {}
        selected_payment_option = None
        for form in form_list:
            if form.__class__.__name__ == "PersonalInfoForm":
                profile_instance = construct_instance(form, profile_instance, form._meta.fields, form._meta.exclude)
                for key, value in form.cleaned_data.items():
                    p_data[key] = value
            elif form.__class__.__name__ == "BankInfoForm":
                bank_instance = construct_instance(form, bank_instance, form._meta.fields, form._meta.exclude)
                if bank_instance:
                    for key, value in form.cleaned_data.items():
                        b_data[key] = value
            elif form.__class__.__name__ == "NomineeInfoForm":
                nominee_instance = construct_instance(form, nominee_instance, form._meta.fields, form._meta.exclude)
                if nominee_instance:
                    for key, value in form.cleaned_data.items():
                        n_data[key] = value
                        pass
                    pass
                pass
            elif form.__class__.__name__ == "CheckOutForm":
                for key, value in form.cleaned_data.items():
                    c_data[key] = value
                    pass
            else:
                for key, value in form.cleaned_data.items():
                    selected_payment_option = value
        if profile_instance:
            obj, created = UserProfile.objects.update_or_create(
                profile_user=self.request.user,
                defaults=p_data,
            )
        if bank_instance:
            obj, created = InvestorBankingDetails.objects.update_or_create(
                investor=self.request.user,
                defaults=b_data,
            )
        if nominee_instance:
            obj, created = InvestorNomineeDetails.objects.update_or_create(
                investor=self.request.user,
                defaults=n_data,
            )

        if selected_payment_option == 'shurjoPay':
            s = ShurjoPay(SurjoPayConfig.MERCHANT_USERNAME, SurjoPayConfig.MERCHANT_PASSWORD,
                          SurjoPayConfig.SHURJOPAY_URL, SurjoPayConfig.DECRYPT_URL,
                          SurjoPayConfig.MERCHANT_PREFIX)
            payment_info = self.make_payment(unit=c_data['cow_quantity'])
            return_url = rest_reverse('sharedfarm:return_url', request=self.request)
            client_ip = get_client_ip(self.request)

            return render(self.request, 'sharedfarm/sp_form.html', {
                'form': s.send_request(client_ip, payment_info.transaction_id, payment_info.total_payable_amount,
                                       return_url)})
            pass
        else:
            payment_info = self.make_payment(unit=c_data['cow_quantity'])
            unit_book_order_payment_email(self.request.user, payment_info.total_payable_amount,
                                          payment_info.unit, self.product)
            pass

        return redirect('core:my_farms')

    def make_payment(self, unit):
        with transaction.atomic():
            transaction_id = f'{SurjoPayConfig.MERCHANT_PREFIX}{round(timezone.now().timestamp())}'

            total_payable_amount = self.product.amount * unit

            payment = Payment.objects.create(total_amount=total_payable_amount,
                                             transaction_id=transaction_id,
                                             created_by=self.request.user)
            invoice = Invoice.objects.create(product=self.product,
                                             amount=total_payable_amount,
                                             user=self.request.user,
                                             payment=payment,
                                             unit=unit)

        payment_info = Map()
        payment_info.payment = payment
        payment_info.transaction_id = transaction_id
        payment_info.total_payable_amount = total_payable_amount
        payment_info.unit = unit
        return payment_info

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        product = Product.objects.get(id=self.kwargs['pk'])

        context.update({'product': product})

        if self.get_cleaned_data_for_step('checkout'):
            order_detail = self.get_cleaned_data_for_step('checkout')
            if product is not None and product.is_cow_available() and order_detail[
                'cow_quantity'] <= product.get_available_number_of_cows():
                order_detail['total'] = product.calculate_total(order_detail['cow_quantity'])

                context.update(order_detail)
        return context

    def get_form_kwargs(self, step):
        kwargs = super(ProductDetailView, self).get_form_kwargs(step)
        if step == 'checkout':
            kwargs['product'] = self.product
        return kwargs

    def post(self, *args, **kwargs):
        """
        This method handles POST requests.
        The wizard will render either the current step (if form validation
        wasn't successful), the next step (if the current step was stored
        successful) or the done view (if no more steps are available)
        """
        # Look for a wizard_goto_step element in the posted data which
        # contains a valid step name. If one was found, render the requested
        # form. (This makes stepping back a lot easier).
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)
        # Check if form was refreshed
        management_form = ManagementForm(self.request.POST, prefix=self.prefix)
        if not management_form.is_valid():
            raise ValidationError(
                _('ManagementForm data is missing or has been tampered.'),
                code='missing_management_form',
            )
        form_current_step = management_form.cleaned_data['current_step']
        if (form_current_step != self.steps.current and
                self.storage.current_step is not None):
            # form refreshed, change current step
            self.storage.current_step = form_current_step
        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        # and try to validate
        if form.is_valid():
            # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(self.steps.current, self.process_step_files(form))
            # check if the current step is the last step
            if self.steps.current == self.steps.last:
                # no more steps, render done view
                # if 'shurjoPay' in self.request.POST:
                #
                #     print(form.cleaned_data)
                return self.render_done(form, **kwargs)

            else:
                # proceed to the next step
                return self.render_next_step(form)
        else:
            if self.steps.current == "checkout":
                msg = f'Info: Only {self.product.get_available_number_of_cows()} units are available to order!'
                messages.warning(self.request, msg)
                return self.render(form)
        return self.render(form)

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'profile':
            userProfile = UserProfile.objects.get(profile_user=self.request.user)

            initial.update(mkdict(
                                  name=getattr(userProfile, 'name'),
                                  profile_img=getattr(userProfile, 'profile_img'),  #NEW Added for adding profile image - 14-03-2022
                                  company_name=getattr(userProfile, 'company_name'),
                                  occupation=getattr(userProfile, 'occupation'),
                                  nationality=getattr(userProfile, 'nationality'),
                                  nid=getattr(userProfile, 'nid'),
                                  dob=getattr(userProfile, 'dob'),
                                  address1=getattr(userProfile, 'address1'),
                                  address2=getattr(userProfile, 'address2'),
                                  zip_code=getattr(userProfile, 'zip_code'),
                                  city=getattr(userProfile, 'city'),
                                  country=getattr(userProfile, 'country')))
        return initial

    def process_step(self, form):
        """
        This method is used to postprocess the form data. By default, it
        returns the raw `form.data` dictionary.
        """

        if self.steps.current == "checkout":
            if self.request.user.userprofile.name and self.request.user.userprofile.company_name and \
                    self.request.user.userprofile.occupation and self.request.user.userprofile.nationality:
                if 'profile' in self.form_list:
                    del self.form_list['profile']

            else:
                pass
            try:
                if self.request.user.investorbankingdetails:
                    if 'bank' in self.form_list:
                        del self.form_list['bank']
            except InvestorBankingDetails.DoesNotExist:
                pass
            try:
                if self.request.user.investornomineedetails:
                    if 'nominee' in self.form_list:
                        del self.form_list['nominee']
            except InvestorNomineeDetails.DoesNotExist:
                pass
            pass
        elif self.steps.current == "profile":
            try:
                if self.request.user.investorbankingdetails:
                    if 'bank' in self.form_list:
                        del self.form_list['bank']
            except InvestorBankingDetails.DoesNotExist:
                pass
        elif self.steps.current == "bank":
            try:
                if self.request.user.investornomineedetails:
                    if 'nominee' in self.form_list:
                        del self.form_list['nominee']
            except InvestorNomineeDetails.DoesNotExist:
                pass
            pass
        return self.get_form_step_data(form)


class BookCreateView(BSModalCreateView):
    template_name = 'sharedfarm/faq.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors)  # , status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


#
# This is used from the ContactPlugin, so could be anywhere on the site. It is
# submitted via AJAX and shouldn't take the user off the page.
#
class SubscriptionView(AjaxableResponseMixin, FormView):
    form_class = SubscriptionForm
    http_method_names = [u'post']  # Not interested in any GETs here...
    template_name = 'sharedfarm/plugins/subscription.html'

    #
    # NOTE: Even though this will never be used, the FormView requires that
    # either the success_url property or the get_success_url() method is
    # defined. So, let use the sensible thing and set it to the page where
    # this plugin is coming from.
    #
    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        # AjaxableResponseMixin expects our contact object to be 'self.object'.
        self.object = form.save(commit=True)
        return super(SubscriptionView, self).form_valid(form)


def mkdict(**kwargs):
    return kwargs


@login_required
def checkout(request, product_id):
    if request.method == "POST" and product_id:
        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            product = None

        form = CheckOutForm(request.POST or None, product=product)
        if form.is_valid():
            unit = form.clean_cow_quantity()

        else:
            unit = None
            msg = f'Info: Only {product.get_available_number_of_cows()} units are available to order!'
            messages.warning(request, msg)
            return redirect('sharedfarm:detail', product_id)

        if product is not None and product.is_cow_available() and unit <= product.get_available_number_of_cows():
            with transaction.atomic():
                s = ShurjoPay(SurjoPayConfig.MERCHANT_USERNAME, SurjoPayConfig.MERCHANT_PASSWORD,
                              SurjoPayConfig.SHURJOPAY_URL, SurjoPayConfig.DECRYPT_URL,
                              SurjoPayConfig.MERCHANT_PREFIX)
                transaction_id = f'{s.merchantPrefix}{round(timezone.now().timestamp())}'

                total_payable_amount = product.amount * unit

                return_url = rest_reverse('sharedfarm:return_url', request=request)
                client_ip = get_client_ip(request)
                payment = Payment.objects.create(total_amount=total_payable_amount,
                                                 transaction_id=transaction_id,
                                                 created_by=request.user)
                invoice = Invoice.objects.create(product=product,
                                                 amount=total_payable_amount,
                                                 user=request.user,
                                                 payment=payment,
                                                 unit=unit)

            return render(request, 'sharedfarm/sp_form.html', {
                'form': s.send_request(client_ip, transaction_id, total_payable_amount, return_url)})


def get_client_ip(req):
    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req.META.get('REMOTE_ADDR')
    return ip


class ReturnUrlView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReturnUrlSerializer

    def get_payment(self):
        self.payment = get_object_or_404(Payment, transaction_id=self.transaction_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data.get('spdata')
        ip = request.META['REMOTE_ADDR']
        url = rest_reverse('sharedfarm:return_url', request=request)
        shurjopay = ShurjoPay(SurjoPayConfig.MERCHANT_USERNAME, SurjoPayConfig.MERCHANT_PASSWORD,
                              SurjoPayConfig.SHURJOPAY_URL, SurjoPayConfig.DECRYPT_URL,
                              SurjoPayConfig.MERCHANT_PREFIX)
        decrypt_data = shurjopay.get_decrypt(response_data)
        parsed_data = json.loads(json.dumps(xmltodict.parse(decrypt_data.text)))
        bankTxStatus = parsed_data["spResponse"]["bankTxStatus"]
        if bankTxStatus not in PayStatus.spChoices:
            bankTxStatus = "FAIL"

        data = mkdict(txID=parsed_data["spResponse"]["txID"],
                      bankTxID=parsed_data["spResponse"]["bankTxID"],
                      bankTxStatus=bankTxStatus,
                      txnAmount=parsed_data["spResponse"]["txnAmount"],
                      spCode=parsed_data["spResponse"]["spCode"],
                      spCodeDes=parsed_data["spResponse"]["spCodeDes"],
                      paymentOption=parsed_data["spResponse"]["paymentOption"], )
        pl_serializer = PaymentLogSerializer(data=data)
        pl_serializer.is_valid(raise_exception=True)
        self.transaction_id = pl_serializer.validated_data['txID']
        self.get_payment()
        if pl_serializer.validated_data['spCode']:
            if self.payment and self.payment.total_amount == \
                    pl_serializer.validated_data['txnAmount'] and pl_serializer.validated_data['spCode'] == '000':

                self.payment.status = PayStatus.COMPLETE
                self.payment.save()
                # user subscription and invoice status updates
                update_user_invoice = Invoice.objects.get(payment=self.payment)
                update_user_invoice.is_paid = True
                update_user_invoice.save()
                order_payment_success_email(update_user_invoice.user, update_user_invoice.amount,
                                            update_user_invoice.unit)

                pass
            else:
                self.payment.status = PayStatus.FAILED
                self.payment.save()

        pl_serializer.save(payment=self.payment)
        toast_data = shurjopay.get_toast_data(parsed_data)
        # return render(request, 'returnurl.html', {'toast': toast_data})
        # return Response(pl_serializer.data, status=status.HTTP_201_CREATED)
        return redirect('sharedfarm:index')


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_fields = ('division',)


class FundOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [AllowAny]


class FaqCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]


class FaqItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FaqItem.objects.all()
    serializer_class = FaqItemSerializer
    filter_class = FaqItemListFilter
    permission_classes = [AllowAny]


class CheckoutRestApiView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = CheckoutResponseSerializer

    def get_queryset(self):
        try:
            product = Product.objects.get(id=self.product.id)

        except Product.DoesNotExist:
            product = None
        return product

    def list(self, request, *args, **kwargs):
        self.request = request
        serializer = CheckoutSerializer(data=kwargs,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.product = serializer.validated_data['product']

        self.unit = serializer.validated_data['unit']

        with transaction.atomic():
            s = ShurjoPay(SurjoPayConfig.MERCHANT_USERNAME, SurjoPayConfig.MERCHANT_PASSWORD,
                          SurjoPayConfig.SHURJOPAY_URL, SurjoPayConfig.DECRYPT_URL,
                          SurjoPayConfig.MERCHANT_PREFIX)
            self.transaction_id = f'{s.merchantPrefix}{round(timezone.now().timestamp())}'
            self.total_payble_amount = self.product.amount * self.unit

            self.return_url = rest_reverse('sharedfarm:return_url', request=self.request)
            self.client_ip = get_client_ip(self.request)

            self.payment, created = Payment.objects.get_or_create(
                transaction_id=self.transaction_id,
                defaults={'total_amount': self.total_payble_amount,
                          'created_by': self.request.user},
            )
            self.invoice, invoice_created = Invoice.objects.get_or_create(
                payment=self.payment,
                defaults={'product': self.product,
                          'amount': self.total_payble_amount,
                          'user': self.request.user,
                          'unit': self.unit,
                          },
            )

            return Response({'txID': self.transaction_id,
                             'form': s.send_request(self.client_ip, self.transaction_id, self.total_payble_amount,
                                                    self.return_url)}, status=status.HTTP_200_OK)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user.pk)


class PaymentCheckOutAPI(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentCheckOutAPISerializer

    def get_payment(self):
        self.payment, created = Payment.objects.get_or_create(
            transaction_id=self.txID,
            defaults={'total_amount': self.txnAmount,
                      'created_by': self.request.user},
        )
        self.invoice, invoice_created = Invoice.objects.get_or_create(
            payment=self.payment,
            defaults={'product': self.product,
                      'amount': self.txnAmount,
                      'user': self.request.user,
                      'unit': self.unit,
                      },
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.txID = serializer.validated_data.get('txID')
        self.bankTxID = serializer.validated_data.get('bankTxID')
        self.spCode = serializer.validated_data.get('spCode')
        self.spCodeDes = serializer.validated_data.get('spCodeDes')
        self.paymentOption = serializer.validated_data.get('paymentOption')
        self.txnAmount = serializer.validated_data.get('txnAmount')
        self.bankTxStatus = serializer.validated_data.get('bankTxStatus')
        self.unit = int(serializer.validated_data.get('unit'))
        self.farm = serializer.validated_data.get('farm')
        self.product = get_object_or_404(Product, pk=self.farm)
        if self.bankTxStatus not in PayStatus.spChoices:
            self.bankTxStatus = "FAIL"

        data = mkdict(txID=self.txID,
                      bankTxID=self.bankTxID,
                      bankTxStatus=self.bankTxStatus,
                      txnAmount=self.txnAmount,
                      spCode=self.spCode,
                      spCodeDes=self.spCodeDes,
                      paymentOption=self.paymentOption, )
        pl_serializer = PaymentLogSerializer(data=data)
        pl_serializer.is_valid(raise_exception=True)
        self.get_payment()
        if pl_serializer.validated_data['spCode']:
            if self.payment and self.payment.total_amount == \
                    pl_serializer.validated_data['txnAmount'] and pl_serializer.validated_data['spCode'] == '000':

                self.payment.status = PayStatus.COMPLETE
                self.payment.save()
                # user subscription and invoice status updates
                update_user_invoice = Invoice.objects.get(payment=self.payment)
                update_user_invoice.is_paid = True
                update_user_invoice.save()
                order_payment_success_email(self.request.user, update_user_invoice.amount, update_user_invoice.unit)
                pass
            else:
                self.payment.status = PayStatus.FAILED
                self.payment.save()

        pl_serializer.save(payment=self.payment)
        # return render(request, 'returnurl.html', {'toast': toast_data})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return redirect('sharedfarm:index')


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        print(order_id)

    elif request.method == 'POST':
        print(request)
    return Response("hi", status=status.HTTP_200_OK)


from djangocms_blog.models import *
from django.http import JsonResponse


def optimize(qs):
    """
    Apply select_related / prefetch_related to optimize the view queries
    :param qs: queryset to optimize
    :return: optimized queryset
    """
    return qs.select_related("app_config").prefetch_related(
        "translations", "categories", "categories__translations", "categories__app_config"
    )


# app_config = AppHookConfigField(BlogConfig, null=True, verbose_name=_("app. config"), blank=True)


def post_queryset(request=None, published_only=True):
    language = get_language()
    posts = Post.objects
    # if app_config:
    #     posts = posts.namespace(app_config.namespace)
    # if current_site:
    #     posts = posts.on_site(get_current_site(request))
    posts = posts.active_translations(language_code=language)
    if (
            published_only
            or not request
            # or not getattr(request, "toolbar", False)
            # or not request.toolbar.edit_mode_active
    ):
        posts = posts.published()
    return optimize(posts.all())


@api_view(['GET'])
def get_posts(request, published_only=True):
    posts = post_queryset(request, published_only)
    # if tags.exists():
    #     posts = posts.filter(tags__in=list(tags.all()))
    # if categories.exists():
    #     posts = posts.filter(categories__in=list(categories.all()))

    return Response(PostSerializer(optimize(posts.distinct())).data, status=status.HTTP_200_OK)


def get_user_invest_summery(user):
    finish_projects = 0
    running_projects = 0
    total_investment = 0
    running_investment = 0
    total_return = 0
    approx_return = 0
    queryset = Invoice.objects.filter(user=user).filter(is_paid=True)
    if queryset:
        for each in queryset:
            running_projects = running_projects + 1
            total_investment = total_investment + each.amount
            running_investment = running_investment + each.amount
            approx_return = approx_return + each.product.calculate_net_profit() if each.product.calculate_net_profit() is not None else 0

    return {"finish_projects": finish_projects,
            "running_projects": running_projects,
            "total_investment": total_investment,
            "running_investment": running_investment,
            "total_return": total_return,
            "approx_return": approx_return}
    pass


class InvestmentSummeryView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = InvestmentSummerySerializer

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user.pk).filter(is_paid=True)

    def list(self, request, *args, **kwargs):
        self.request = request
        finish_projects = 0
        running_projects = 0
        total_investment = 0
        running_investment = 0
        total_return = 0
        approx_return = 0

        queryset = self.filter_queryset(self.get_queryset())

        if queryset:
            for each in queryset:
                running_projects = running_projects + 1
                total_investment = total_investment + each.amount
                running_investment = running_investment + each.amount
                approx_return = approx_return + each.product.calculate_net_profit() if each.product.calculate_net_profit() is not None else 0

        return Response({"finish_projects": finish_projects,
                         "running_projects": running_projects,
                         "total_investment": total_investment,
                         "running_investment": running_investment,
                         "total_return": total_return,
                         "approx_return": approx_return}, status=status.HTTP_200_OK)


class WhatsNewBannerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WhatsNewBannerSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return WhatsNewBanner.objects.filter(is_active=True)
