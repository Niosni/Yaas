# Generated by Django 2.1.2 on 2018-10-30 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0003_auto_20181030_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='orig_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='bid_price',
        ),
    ]
