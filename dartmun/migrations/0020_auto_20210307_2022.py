# Generated by Django 3.1.6 on 2021-03-07 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0019_auto_20210306_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='writingmanager',
            name='resolutions',
        ),
        migrations.RemoveField(
            model_name='writingmanager',
            name='working_papers',
        ),
        migrations.DeleteModel(
            name='TallyGroup',
        ),
    ]
