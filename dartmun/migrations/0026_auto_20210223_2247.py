# Generated by Django 3.1.6 on 2021-02-23 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0025_parlipromanager_current_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motionentry',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.topic'),
        ),
    ]
