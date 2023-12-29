# Generated by Django 4.2.4 on 2023-12-29 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delay_reporting', '0005_alter_delayreport_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delayreport',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]