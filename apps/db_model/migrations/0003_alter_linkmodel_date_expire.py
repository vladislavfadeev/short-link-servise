# Generated by Django 4.2.2 on 2023-06-07 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0002_linkmodel_last_changed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmodel',
            name='date_expire',
            field=models.DateField(blank=True, null=True),
        ),
    ]
