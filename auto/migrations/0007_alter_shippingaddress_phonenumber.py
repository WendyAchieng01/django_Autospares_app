# Generated by Django 3.2.25 on 2024-03-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0006_shippingaddress_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='phonenumber',
            field=models.CharField(max_length=20),
        ),
    ]