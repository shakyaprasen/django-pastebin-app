# Generated by Django 2.1.1 on 2018-10-04 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pastebin', '0005_auto_20181003_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_no',
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
