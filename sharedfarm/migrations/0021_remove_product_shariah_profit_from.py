# Generated by Django 3.1.11 on 2022-05-31 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharedfarm', '0020_auto_20220519_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shariah_profit_from',
        ),
    ]
