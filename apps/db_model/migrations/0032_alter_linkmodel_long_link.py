# Generated by Django 4.2.3 on 2023-08-02 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0031_alter_grouplinkmodel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmodel',
            name='long_link',
            field=models.CharField(max_length=30000),
        ),
    ]
