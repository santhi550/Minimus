# Generated by Django 2.2.3 on 2020-07-11 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20200710_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='availability',
            field=models.BooleanField(default=False),
        ),
    ]