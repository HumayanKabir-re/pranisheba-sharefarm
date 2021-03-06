# Generated by Django 3.1.11 on 2022-03-07 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_merge_20220125_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestorInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_info', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.investorbankingdetails')),
                ('nominiee_info', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.investornomineedetails')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
            ],
        ),
    ]
