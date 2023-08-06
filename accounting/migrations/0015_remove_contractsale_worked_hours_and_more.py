# Generated by Django 4.2.2 on 2023-07-22 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_contracttype_field_attributes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractsale',
            name='worked_hours',
        ),
        migrations.RemoveField(
            model_name='contractsalesinvoice',
            name='contract',
        ),
        migrations.AddField(
            model_name='contractsale',
            name='sales_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 29, 20, 48, 56, 620169, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 5, 20, 48, 56, 619171, tzinfo=datetime.timezone.utc), help_text='date of delivery'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 29, 20, 48, 56, 619171, tzinfo=datetime.timezone.utc), help_text='milestone due date'),
        ),
    ]
