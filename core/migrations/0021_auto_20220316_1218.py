# Generated by Django 3.1.11 on 2022-03-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20220316_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(blank=True, help_text='Year-Month-Day', null=True, verbose_name='Year-Month-Day'),
        ),
    ]
