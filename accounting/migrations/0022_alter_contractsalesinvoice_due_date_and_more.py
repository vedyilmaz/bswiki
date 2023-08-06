# Generated by Django 4.2.2 on 2023-08-05 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0021_alter_contractsalesinvoice_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 12, 17, 42, 52, 983387, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 19, 17, 42, 52, 982391, tzinfo=datetime.timezone.utc), help_text='date of delivery'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 12, 17, 42, 52, 982391, tzinfo=datetime.timezone.utc), help_text='milestone due date'),
        ),
    ]