# Generated by Django 2.1.7 on 2019-02-27 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0008_auto_20190221_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('fi', 'Finnish')], default='en', max_length=10),
        ),
    ]
