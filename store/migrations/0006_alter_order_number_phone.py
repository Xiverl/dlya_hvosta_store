# Generated by Django 3.2.16 on 2023-09-09 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_order_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number_phone',
            field=models.CharField(max_length=11, verbose_name='Номер телефона'),
        ),
    ]
