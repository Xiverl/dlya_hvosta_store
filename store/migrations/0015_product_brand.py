# Generated by Django 3.2.16 on 2023-09-18 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20230916_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.brand', verbose_name='Производитель'),
            preserve_default=False,
        ),
    ]
