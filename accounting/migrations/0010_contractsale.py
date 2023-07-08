# Generated by Django 4.2.2 on 2023-07-08 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_bankaccount_rename_contracts_contract_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='date')),
                ('worked_hours', models.FloatField()),
                ('amount', models.FloatField()),
                ('note', models.TextField(blank=True)),
                ('contracts', models.ManyToManyField(to='accounting.contract')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
