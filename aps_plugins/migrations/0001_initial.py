# Generated by Django 3.1.11 on 2021-06-17 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericTitleDescription',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aps_plugins_generictitledescription', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Generic Title & Description',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Section_With_Image_background',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aps_plugins_section_with_image_background', serialize=False, to='cms.cmsplugin')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(upload_to='section_with_image_background')),
            ],
            options={
                'verbose_name': 'Section with Image Background',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='StakeHolderDetails',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aps_plugins_stakeholderdetails', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(max_length=200)),
                ('icon', models.CharField(blank=True, choices=[('bi bi-people', 'Farmers'), ('bi bi-cash-coin', 'Investors'), ('bi bi-bank2', 'Agri Companies'), ('bi bi-cart-check', 'Buyers')], max_length=100, null=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Stakeholder details',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='WhatWeDo',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aps_plugins_whatwedo', serialize=False, to='cms.cmsplugin')),
                ('image', models.ImageField(upload_to='what_we_do')),
                ('head', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'What We Do',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='WhoWeAreLandingText',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='aps_plugins_whowearelandingtext', serialize=False, to='cms.cmsplugin')),
                ('text1', models.CharField(blank=True, max_length=200, null=True)),
                ('text2', models.CharField(blank=True, max_length=200, null=True)),
                ('text3', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Who we are landing text',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
