# Generated by Django 3.1.6 on 2021-02-21 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0016_auto_20210221_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parlipromanager',
            name='current_mode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.debatemode'),
        ),
    ]
