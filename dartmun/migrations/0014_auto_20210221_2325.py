# Generated by Django 3.1.6 on 2021-02-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0013_auto_20210221_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motion',
            name='vote_simple',
        ),
        migrations.AddField(
            model_name='motion',
            name='vote_type',
            field=models.CharField(choices=[('simple', 'simple majority'), ('2/3', '2/3 majority')], default='simple', max_length=16),
        ),
    ]
