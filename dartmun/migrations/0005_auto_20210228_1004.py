# Generated by Django 3.1.6 on 2021-02-28 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0004_auto_20210227_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parlipromanager',
            name='caucus_until',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
