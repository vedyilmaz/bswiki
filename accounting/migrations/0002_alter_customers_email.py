# Generated by Django 4.2.2 on 2023-07-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='email',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
