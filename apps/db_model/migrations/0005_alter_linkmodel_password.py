# Generated by Django 4.2.2 on 2023-06-07 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0004_alter_linkmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmodel',
            name='password',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
