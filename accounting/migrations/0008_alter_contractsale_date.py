# Generated by Django 4.2.2 on 2023-07-15 21:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_alter_contractsale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsale',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 15, 21, 0, 27, 31359, tzinfo=datetime.timezone.utc), help_text='date'),
        ),
    ]