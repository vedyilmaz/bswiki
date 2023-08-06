# Generated by Django 4.2.2 on 2023-07-23 00:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0017_remove_contractsalesinvoice_contract_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractsalesinvoice',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.contract'),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 30, 0, 46, 9, 846385, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 6, 0, 46, 9, 846385, tzinfo=datetime.timezone.utc), help_text='date of delivery'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 30, 0, 46, 9, 846385, tzinfo=datetime.timezone.utc), help_text='milestone due date'),
        ),
    ]
