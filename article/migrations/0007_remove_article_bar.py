# Generated by Django 2.2.12 on 2021-11-03 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20211103_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='bar',
        ),
    ]