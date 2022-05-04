# Generated by Django 3.2.7 on 2022-04-28 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import src.client.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('profile', models.ImageField(blank=True, upload_to=src.client.models.upload_location)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]