# Generated by Django 3.1.6 on 2021-03-30 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0039_auto_20210330_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='amendment',
            name='introduced',
            field=models.BooleanField(default=False),
        ),
    ]
