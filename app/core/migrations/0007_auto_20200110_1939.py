# Generated by Django 3.0.2 on 2020-01-10 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_advertising_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertising',
            name='fromDate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='advertising',
            name='toDate',
            field=models.DateTimeField(blank=True),
        ),
    ]
