# Generated by Django 3.1.6 on 2021-02-21 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0007_auto_20210221_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='tallyscore',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.tallycategory'),
        ),
    ]
