# Generated by Django 3.1.6 on 2021-03-13 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0023_auto_20210309_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tallycategoryscore',
            name='tallies',
        ),
        migrations.AddField(
            model_name='committeetallycategory',
            name='points_possible',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
