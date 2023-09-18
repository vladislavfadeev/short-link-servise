# Generated by Django 4.2.2 on 2023-07-18 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0021_alter_linkmodel_group_alter_linkmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouplinkmodel',
            name='date_expire',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='linkmodel',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='db_model.grouplinkmodel'),
        ),
    ]
