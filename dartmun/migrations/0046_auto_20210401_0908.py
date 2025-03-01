# Generated by Django 3.1.6 on 2021-04-01 00:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dartmun', '0045_auto_20210331_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chair',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='chair',
            name='major',
        ),
        migrations.AddField(
            model_name='chair',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Secretariat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=64, null=True)),
                ('year', models.PositiveSmallIntegerField(default=2024, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='conference',
            name='secretariat',
            field=models.ManyToManyField(to='dartmun.Secretariat'),
        ),
    ]
