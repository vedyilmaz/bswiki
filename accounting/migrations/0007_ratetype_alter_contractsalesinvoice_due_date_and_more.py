# Generated by Django 4.2.2 on 2023-07-21 23:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_alter_contractsalesinvoice_due_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_type', models.CharField(max_length=100, verbose_name='sales_ids')),
                ('billing_period', models.CharField(max_length=100, verbose_name='sales_ids')),
                ('note', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 28, 23, 53, 40, 281446, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 4, 23, 53, 40, 281446, tzinfo=datetime.timezone.utc), help_text='date of delivery'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 28, 23, 53, 40, 281446, tzinfo=datetime.timezone.utc), help_text='milestone due date'),
        ),
    ]
