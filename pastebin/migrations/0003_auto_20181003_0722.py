# Generated by Django 2.1.1 on 2018-10-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pastebin', '0002_auto_20181002_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='url_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
