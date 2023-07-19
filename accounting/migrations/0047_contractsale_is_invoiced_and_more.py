# Generated by Django 4.2.2 on 2023-07-18 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0046_alter_contractsalesinvoice_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractsale',
            name='is_invoiced',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 25, 17, 20, 51, 647113, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
    ]
