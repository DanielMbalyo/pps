# Generated by Django 3.2.7 on 2022-06-23 07:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('billing', '0002_auto_20220622_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='charge',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
            preserve_default=False,
        ),
    ]