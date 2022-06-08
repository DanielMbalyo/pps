# Generated by Django 3.2.7 on 2022-06-08 12:03

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
                ('first', models.CharField(blank=True, max_length=200)),
                ('middle', models.CharField(blank=True, max_length=200, null=True)),
                ('last', models.CharField(blank=True, max_length=200)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='unspecified', max_length=200)),
                ('dob', models.DateField()),
                ('citizenship', models.CharField(blank=True, default='Tanzanian', max_length=200)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('martial', models.CharField(choices=[('single', 'Single'), ('relation', 'In Relation'), ('married', 'Married'), ('divorsed', 'Divorsed')], default='single', max_length=200)),
                ('identification', models.CharField(choices=[('none', 'None'), ('nida', 'National ID'), ('voters id', 'Voters ID'), ('licence', 'Driving Licence')], default='single', max_length=200)),
                ('id_number', models.CharField(default='00000000000000', max_length=200)),
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
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('employment', 'Employment'), ('consultant', 'Consultant'), ('business', 'Business')], default='employed', max_length=200)),
                ('employer', models.CharField(default='None', max_length=200)),
                ('branch', models.CharField(blank=True, max_length=200, null=True)),
                ('referee', models.CharField(default='0712345743', max_length=200)),
                ('duration', models.CharField(default='1', max_length=200)),
                ('range', models.FloatField(default=0.0, max_length=200)),
                ('dependants', models.CharField(blank=True, default='0', max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
