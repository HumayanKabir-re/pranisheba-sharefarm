# Generated by Django 3.1.11 on 2021-08-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aps_plugins', '0008_auto_20210825_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stakeholderdetails',
            name='description',
            field=models.TextField(),
        ),
    ]