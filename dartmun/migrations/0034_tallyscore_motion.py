# Generated by Django 3.1.6 on 2021-03-23 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0033_gradesmanager_committee_average'),
    ]

    operations = [
        migrations.AddField(
            model_name='tallyscore',
            name='motion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.motion'),
        ),
    ]
