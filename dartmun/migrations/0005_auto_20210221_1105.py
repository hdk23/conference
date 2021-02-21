# Generated by Django 3.1.6 on 2021-02-21 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0004_auto_20210221_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoremanager',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tallycategoryscore',
            name='raw_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='tallycategoryscore',
            name='scaled_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tallycategoryscore',
            name='zscore',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
