# Generated by Django 4.2.2 on 2023-06-26 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db_model', '0011_alter_groupstatistics_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupstatistics',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_model.grouplinkmodel'),
        ),
        migrations.AlterField(
            model_name='statisticsmodel',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_stat', to='db_model.linkmodel'),
        ),
        migrations.CreateModel(
            name='LinkStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_model.linkmodel')),
            ],
        ),
        migrations.CreateModel(
            name='AccountStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]