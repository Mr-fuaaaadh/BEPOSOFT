# Generated by Django 5.1 on 2024-10-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beposoft_app', '0045_alter_order_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='code_charge',
            field=models.IntegerField(default=0),
        ),
    ]