# Generated by Django 5.0.2 on 2024-02-19 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('Present_address', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=100, null=True)),
                ('details', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
