# Generated by Django 3.1.6 on 2021-03-05 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dartmun', '0016_auto_20210305_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduced', models.BooleanField(default=False)),
                ('votes_for', models.PositiveSmallIntegerField(null=True)),
                ('votes_against', models.PositiveSmallIntegerField(null=True)),
                ('votes_abstain', models.PositiveSmallIntegerField(null=True)),
                ('passed', models.BooleanField(null=True)),
                ('rubric_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.rubricentry')),
                ('signatories', models.ManyToManyField(related_name='reso_signatories', to='dartmun.Delegation')),
                ('sponsors', models.ManyToManyField(related_name='reso_sponsors', to='dartmun.Delegation')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.topic')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduced', models.BooleanField(default=False)),
                ('signatories', models.ManyToManyField(related_name='wp_signatories', to='dartmun.Delegation')),
                ('sponsors', models.ManyToManyField(related_name='wp_sponsors', to='dartmun.Delegation')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.topic')),
            ],
        ),
        migrations.CreateModel(
            name='WritingManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_reso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_reso', to='dartmun.resolution')),
                ('current_wp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_wp', to='dartmun.workingpaper')),
                ('resolutions', models.ManyToManyField(to='dartmun.Resolution')),
                ('working_papers', models.ManyToManyField(related_name='committee_wps', to='dartmun.WorkingPaper')),
            ],
        ),
        migrations.AddField(
            model_name='committee',
            name='writing',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.writingmanager'),
        ),
    ]
