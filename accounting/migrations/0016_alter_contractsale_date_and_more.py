# Generated by Django 4.2.2 on 2023-07-15 22:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0015_alter_contractsale_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsale',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 15, 22, 21, 25, 323175, tzinfo=datetime.timezone.utc), help_text='date'),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 15, 22, 21, 25, 323175, tzinfo=datetime.timezone.utc), help_text='invoice date'),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 22, 22, 21, 25, 323175, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
    ]
