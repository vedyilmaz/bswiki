# Generated by Django 4.2.2 on 2023-07-18 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0039_alter_contractsalesinvoice_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 25, 14, 46, 38, 406030, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
    ]
