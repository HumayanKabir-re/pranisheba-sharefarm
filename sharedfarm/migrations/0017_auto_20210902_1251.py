# Generated by Django 3.1.11 on 2021-09-02 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharedfarm', '0016_auto_20210902_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='howweworkhead',
            name='number_of_steps',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='howweworkstepitem',
            name='step_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
