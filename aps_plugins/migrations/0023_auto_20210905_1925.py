# Generated by Django 3.1.11 on 2021-09-05 13:25

from django.db import migrations
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aps_plugins', '0022_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourcompany',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True),
        ),
    ]
