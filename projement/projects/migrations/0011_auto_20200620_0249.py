# Generated by Django 2.2 on 2020-06-19 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20200620_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='project',
            field=models.ManyToManyField(related_name='tags', through='projects.ProjectTag', to='projects.Project'),
        ),
    ]
