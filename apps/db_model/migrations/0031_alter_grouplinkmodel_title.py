# Generated by Django 4.2.3 on 2023-08-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0030_alter_grouplinkmodel_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplinkmodel',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]