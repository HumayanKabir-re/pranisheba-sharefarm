# Generated by Django 3.1.11 on 2021-06-27 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharedfarm', '0005_invoice_payment_paymentlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='comment',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=64, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sharedfarm.payment'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_product', to='sharedfarm.product'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
