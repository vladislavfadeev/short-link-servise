# Generated by Django 4.2.2 on 2023-06-26 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_model', '0009_alter_statisticsmodel_browser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_model.grouplinkmodel')),
            ],
        ),
    ]
