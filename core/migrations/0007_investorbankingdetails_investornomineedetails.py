# Generated by Django 3.1.11 on 2022-01-17 08:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220113_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestorNomineeDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=' Please enter the Nominee Name', max_length=100, verbose_name='Nominee Name')),
                ('relationship', models.CharField(help_text=' Relationship with Nominee.', max_length=255, verbose_name='Relationship with Nominee')),
                ('contact_no', models.CharField(help_text='Nominee Contact number', max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '01912345678'. Up to 11 digits allowed.", regex='[^1-9][1][0-9]{9,9}\\b')])),
                ('nid', models.CharField(max_length=17, verbose_name='National ID')),
                ('investor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestorBankingDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=' Please enter the Bank Name', max_length=100, verbose_name='Bank Name')),
                ('branch_name', models.CharField(help_text=' Please enter the Bank Branch Name.', max_length=100, verbose_name='Bank Branch Name')),
                ('account_no', models.CharField(help_text=' Please enter the Bank Account Number', max_length=100, verbose_name='Bank Account Number')),
                ('Account_name', models.CharField(max_length=100, verbose_name='Account Name')),
                ('investor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]