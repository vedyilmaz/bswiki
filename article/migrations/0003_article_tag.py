# Generated by Django 2.2.7 on 2019-11-14 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20191113_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
