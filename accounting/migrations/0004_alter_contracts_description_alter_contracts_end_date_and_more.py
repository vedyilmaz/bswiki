# Generated by Django 4.2.2 on 2023-07-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_remove_contracts_due_date_contracts_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='end_date',
            field=models.DateField(help_text='contract end date', null=True),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
