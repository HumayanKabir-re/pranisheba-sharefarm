# Generated by Django 3.1.11 on 2021-08-23 19:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('aps_plugins', '0002_teammember'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurCompany',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aps_plugins_ourcompany', serialize=False, to='cms.cmsplugin')),
                ('thumb1', models.ImageField(upload_to='our_company')),
                ('thumb2', models.ImageField(upload_to='our_company')),
                ('thumb3', models.ImageField(upload_to='our_company')),
                ('thumb4', models.ImageField(upload_to='our_company')),
                ('Video_thumb', models.ImageField(upload_to='our_company')),
                ('video_url', models.URLField(help_text='Please enter your video url', validators=[django.core.validators.URLValidator])),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Our Company',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
