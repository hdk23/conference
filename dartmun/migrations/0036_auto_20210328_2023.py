# Generated by Django 3.1.6 on 2021-03-28 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0035_advisor_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('acronym', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('counts', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='delegate',
            name='number',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('acronym', models.CharField(max_length=16, null=True)),
                ('organs', models.ManyToManyField(to='dartmun.Organ')),
                ('sessions', models.ManyToManyField(to='dartmun.Session')),
            ],
        ),
    ]
