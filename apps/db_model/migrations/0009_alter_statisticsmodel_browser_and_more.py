# Generated by Django 4.2.2 on 2023-06-26 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0008_rename_linktransitionsmodel_statisticsmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statisticsmodel',
            name='browser',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='statisticsmodel',
            name='device',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='statisticsmodel',
            name='os',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='statisticsmodel',
            name='ref_link',
            field=models.CharField(max_length=30000, null=True),
        ),
    ]
