# Generated by Django 2.1.1 on 2018-10-03 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pastebin', '0004_url_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='url',
            new_name='short_url',
        ),
    ]
