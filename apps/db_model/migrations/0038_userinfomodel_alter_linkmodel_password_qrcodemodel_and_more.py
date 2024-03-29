# Generated by Django 4.2.3 on 2023-08-08 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db_model', '0037_alter_linkmodel_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agent_unparsed', models.CharField(default='Not defined', max_length=150)),
                ('fingerprint', models.TextField(blank=True, null=True)),
                ('device', models.CharField(default='Not defined', max_length=20)),
                ('os', models.CharField(default='Not defined', max_length=20)),
                ('browser', models.CharField(default='Not defined', max_length=20)),
                ('ref_link', models.CharField(default='Not defined', max_length=30000)),
                ('user_ip', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='linkmodel',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.CreateModel(
            name='QRCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('text', models.CharField(max_length=550)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_model.userinfomodel')),
            ],
        ),
        migrations.AddField(
            model_name='grouplinkmodel',
            name='user_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_model.userinfomodel'),
        ),
        migrations.AddField(
            model_name='linkmodel',
            name='user_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='db_model.userinfomodel'),
        ),
    ]
