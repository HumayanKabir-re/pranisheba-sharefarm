# from rest_framework.serializers import ModelSerializer, Serializer, ValidationError
from rest_framework import serializers
from .models import *
# from cattle.models import Invoice
from django.utils.translation import ugettext_lazy as _
from rest_framework.generics import get_object_or_404


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    division = DivisionSerializer()

    class Meta:
        model = District
        exclude = ('lat', 'lon', 'website')


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'


class FaqItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqItem
        fields = '__all__'


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    available_cow = serializers.SerializerMethodField()
    location = DistrictSerializer()
    breed = BreedSerializer()

    class Meta:
        model = Product
        exclude = ('app_config',)

    def get_available_cow(self, obj):
        return obj.get_available_number_of_cows()


class InvoiceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Invoice
        fields = '__all__'


class WhatsNewBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsNewBanner
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):
    status = serializers.CharField()
    txID = serializers.CharField()
    bankTxID = serializers.CharField()
    paymentOption = serializers.CharField()
    txnAmount = serializers.DecimalField(max_digits=12, decimal_places=2)


class ReturnUrlSerializer(serializers.Serializer):
    spdata = serializers.CharField()


class PaymentCheckOutAPISerializer(serializers.Serializer):
    txID = serializers.CharField(label=_('txID'), required=True,
                                 help_text="Transaction ID.")
    bankTxID = serializers.CharField(label=_('bankTxID'),
                                     help_text="Bank Transaction ID.")
    bankTxStatus = serializers.CharField(label=_('bankTxStatus'),
                                         help_text="Bank Transaction Status.")
    txnAmount = serializers.DecimalField(max_digits=12, decimal_places=2, label=_('txnAmount'), required=True,
                                         help_text="Transaction Amount.")
    spCode = serializers.CharField(label=_('spCode'), required=True,
                                   help_text="ShurjoPay Code.")
    spCodeDes = serializers.CharField(label=_('spCodeDes'),
                                      help_text="ShurjoPay Code.")
    paymentOption = serializers.CharField(label=_('spCodeDes'),
                                          help_text="ShurjoPay Code description.")
    farm = serializers.CharField(label=_('farm'), required=True,
                                 help_text="Fund Opportunities object id.")
    unit = serializers.DecimalField(label=_('unit'), required=True, max_digits=64, decimal_places=2,
                                    help_text="Number of unit.")


class ReturnUrlResponseSerializer(serializers.Serializer):
    txID = serializers.CharField()


class CheckoutResponseSerializer(serializers.Serializer):
    txID = serializers.CharField(max_length=200)
    form = serializers.CharField(max_length=1000)


class InvestmentSummerySerializer(serializers.Serializer):
    finish_projects = serializers.IntegerField()
    running_projects = serializers.IntegerField()
    total_investment = serializers.DecimalField(label=_('total_investment'), max_digits=64, decimal_places=2,
                                                help_text="Total Investment.")
    running_investment = serializers.DecimalField(label=_('running_investment'), max_digits=64, decimal_places=2,
                                                  help_text="Running Investment.")
    total_return = serializers.DecimalField(label=_('total_return'), max_digits=64, decimal_places=2,
                                            help_text="Total Return")

    approx_return = serializers.DecimalField(label=_('approx_return'), max_digits=64, decimal_places=2,
                                             help_text="Approx return.")


class CheckoutSerializer(serializers.Serializer):
    farm = serializers.CharField(label=_('farm'), required=True,
                                 help_text="Fund Opportunities object id.")
    unit = serializers.DecimalField(label=_('unit'), required=True, max_digits=64, decimal_places=2,
                                    help_text="Number of unit.")

    #
    # comment = serializers.CharField(label=_("comment"),
    #                                 help_text="subscription plan amount.", required=False)

    def validate(self, attrs):
        product_id = attrs.get('farm')
        product_obj = get_object_or_404(Product, pk=product_id)
        unit = int(attrs.get('unit'))
        attrs['product'] = product_obj
        attrs['unit'] = unit
        if unit > product_obj.get_available_number_of_cows():
            raise serializers.ValidationError(
                f'Out of stock! Your max unit limit: {product_obj.get_available_number_of_cows()}.')
        # attrs['comment'] = attrs.get('comment')
        return attrs


from djangocms_blog.models import *


class PostSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = Post
        exclude = ('categories', 'sites', 'related')
