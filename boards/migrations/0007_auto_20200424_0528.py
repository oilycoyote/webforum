# Generated by Django 3.0.5 on 2020-04-24 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_remove_post_board'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('edit_post', 'Edit post'),)},
        ),
    ]