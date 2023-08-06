# Generated by Django 4.2.2 on 2023-07-22 19:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0009_billingperiod_alter_contractsalesinvoice_due_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='description',
            new_name='note',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='rate_type',
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_name',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractsale',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractsalesinvoice',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractsalestransaction',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_alias',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='rate_amount',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='contractsalesinvoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 29, 19, 0, 56, 941420, tzinfo=datetime.timezone.utc), help_text='invoice due date'),
        ),
        migrations.AlterField(
            model_name='contractsalestransaction',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.contractsalesinvoice'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 5, 19, 0, 56, 941420, tzinfo=datetime.timezone.utc), help_text='date of delivery'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 29, 19, 0, 56, 941420, tzinfo=datetime.timezone.utc), help_text='milestone due date'),
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(max_length=100, verbose_name='Billing period')),
                ('note', models.TextField(blank=True)),
                ('rate_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.ratetype')),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounting.contracttype'),
        ),
    ]