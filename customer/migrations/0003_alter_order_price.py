# Generated by Django 4.1.5 on 2023-06-15 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_rename_items_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
