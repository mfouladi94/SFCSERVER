# Generated by Django 4.2.4 on 2023-12-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delay_reporting', '0006_alter_delayreport_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
