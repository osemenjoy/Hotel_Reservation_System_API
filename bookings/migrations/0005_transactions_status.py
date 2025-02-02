# Generated by Django 5.1.5 on 2025-02-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_alter_booking_status_transactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='status',
            field=models.CharField(choices=[('SUCCESSFUL', 'Successful'), ('FAILED', 'Failed')], default='successful', max_length=50),
            preserve_default=False,
        ),
    ]
