# Generated by Django 3.0.5 on 2020-04-18 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20200418_0637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views_counter',
        ),
        migrations.AddField(
            model_name='topic',
            name='views_counter',
            field=models.IntegerField(default=0),
        ),
    ]
