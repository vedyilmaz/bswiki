# Generated by Django 4.2.2 on 2023-07-15 20:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_alter_contractsale_date_alter_milestone_contract_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsale',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 7, 15, 20, 39, 4, 568765, tzinfo=datetime.timezone.utc), help_text='date'),
        ),
    ]