# Generated by Django 3.2.16 on 2023-11-19 12:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20231023_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='number_phone',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Номер телефона пользователя содержит недопустимый символ', regex='^((8|\\+7)[\\- ]?)?(\\(?\\d{3}\\)?[\\- ]?)?[\\d\\- ]{7,10}$')], verbose_name='Номер телефона'),
        ),
    ]
