# Generated by Django 4.2.3 on 2023-09-10 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0041_alter_grouplinkmodel_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmodel',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='db_model.grouplinkmodel'),
        ),
    ]