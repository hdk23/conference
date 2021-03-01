# Generated by Django 3.1.6 on 2021-03-01 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0009_caucusmanager_spoke'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubricentry',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.topic'),
        ),
        migrations.AddField(
            model_name='tallyscore',
            name='rubric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.rubricentry'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='max_possible',
            field=models.FloatField(default=0),
        ),
    ]
