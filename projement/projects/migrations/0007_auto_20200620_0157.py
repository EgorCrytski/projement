# Generated by Django 2.2 on 2020-06-19 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200620_0131'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectsTags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]