# Generated by Django 3.1.11 on 2022-03-15 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_userprofile_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dob',
        ),
    ]