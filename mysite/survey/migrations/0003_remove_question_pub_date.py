# Generated by Django 2.0.5 on 2018-05-23 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_userresponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
    ]
