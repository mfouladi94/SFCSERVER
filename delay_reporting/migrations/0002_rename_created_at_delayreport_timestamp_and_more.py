# Generated by Django 4.2.4 on 2023-12-29 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_remove_trip_order_alter_trip_status_delete_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delay_reporting', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delayreport',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='delayreport',
            name='assigned_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='delayreport',
            name='is_trip_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='delayreport',
            name='reason',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='trip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trips.trip'),
        ),
        migrations.AlterField(
            model_name='delayreport',
            name='delay_minutes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]