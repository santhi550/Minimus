# Generated by Django 2.2.3 on 2020-07-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='url',
            field=models.CharField(max_length=1000, verbose_name='URL'),
        ),
    ]
