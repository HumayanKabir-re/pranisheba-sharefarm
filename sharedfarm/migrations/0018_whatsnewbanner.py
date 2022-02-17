# Generated by Django 3.1.11 on 2022-01-13 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sharedfarm', '0017_auto_20210902_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsNewBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='whats_new')),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='whats_new_product', to='sharedfarm.product')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]