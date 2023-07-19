# Generated by Django 4.2.2 on 2023-07-16 09:39

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0021_alter_contractsale_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsale',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='date'),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='invoice date'),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 23, 9, 39, 10, 746931, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
    ]