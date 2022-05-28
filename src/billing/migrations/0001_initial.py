# Generated by Django 3.2.7 on 2022-05-28 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.CharField(blank=True, max_length=120, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('refunded', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('currency', models.CharField(default='TZS', max_length=120)),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=120)),
                ('brand', models.CharField(blank=True, max_length=120, null=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('exp_month', models.IntegerField(blank=True, null=True)),
                ('exp_year', models.IntegerField(blank=True, null=True)),
                ('last4', models.CharField(blank=True, max_length=4, null=True)),
                ('default', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile')),
            ],
        ),
    ]
