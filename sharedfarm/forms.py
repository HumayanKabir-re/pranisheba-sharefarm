from django import forms
from .models import Product, FundCategory, Faq, Subscription
from django.utils.translation import ugettext as _, ungettext, ugettext_lazy
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib import messages


class BookModelForm(BSModalModelForm):
    class Meta:
        model = Faq
        fields = ['category', ]


class DropdownModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category',)
        widgets = {
            'category': forms.Select(choices=((None,
                                               ugettext_lazy("Select Offering Category")),) + FundCategory.TYPE)
        }


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email', ]


class CheckOutForm(forms.Form):
    cow_quantity = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', )
        super(CheckOutForm, self).__init__(*args, **kwargs)

    def clean_cow_quantity(self):
        cow_quantity = self.cleaned_data['cow_quantity']

        if cow_quantity <= self.product.get_available_number_of_cows():
            pass
        else:
            raise forms.ValidationError("Out of stock")

        return cow_quantity


class CheckOutConfirmationForm(forms.Form):
    CHOICES = [('bankPay', 'bankPay'), ('shurjoPay', 'shurjoPay')]
    paymentOption = forms.ChoiceField(label='Payment Option', widget=forms.RadioSelect(), choices=CHOICES,
                                      required=False)

    def clean_paymentOption(self):
        data = self.cleaned_data.get('paymentOption')
        if not data:
            self.add_error("paymentOption", "Please select one of these Payment options")
        return data
