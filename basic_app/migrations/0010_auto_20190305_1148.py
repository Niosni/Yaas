# Generated by Django 2.1.5 on 2019-03-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0009_userprofileinfo_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='language',
            field=models.CharField(max_length=4),
        ),
    ]
