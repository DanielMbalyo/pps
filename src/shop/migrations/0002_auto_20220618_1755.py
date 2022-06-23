# Generated by Django 3.2.7 on 2022-06-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='location',
            new_name='district',
        ),
        migrations.AddField(
            model_name='shop',
            name='street',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='region',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='street',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]