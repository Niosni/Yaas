# Generated by Django 2.1.5 on 2019-01-24 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0005_auto_20190124_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='author',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='auction',
            name='bidder',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]