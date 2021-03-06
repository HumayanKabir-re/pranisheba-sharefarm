# Generated by Django 3.1.11 on 2021-06-20 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Full name')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('country', models.CharField(max_length=1024, verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Full Address',
                'verbose_name_plural': 'Full Addresses',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_img', models.ImageField(default='img/profile_img', upload_to='profile_user')),
                ('name', models.CharField(blank=True, help_text=' Please enter the Full Name according to NID', max_length=30, verbose_name='Full Name')),
                ('nid', models.CharField(blank=True, max_length=17, null=True, verbose_name='National ID')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.userlocation')),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
