# Generated by Django 3.1.6 on 2021-02-24 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeDirector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chair', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dartmun.chair')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chair', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dartmun.chair')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeTallyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average', models.FloatField(blank=True, null=True)),
                ('stdev', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criterion', models.CharField(max_length=64)),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CriterionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.criterion')),
            ],
        ),
        migrations.CreateModel(
            name='DebateMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(max_length=64)),
                ('acronym', models.CharField(max_length=8)),
                ('speeches', models.BooleanField(default=False)),
                ('yielding', models.BooleanField(default=False)),
                ('duration', models.BooleanField(default=False)),
                ('speaking_time', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('present', models.BooleanField(null=True)),
                ('voting', models.BooleanField(null=True)),
                ('delegates', models.ManyToManyField(to='dartmun.Delegate')),
            ],
        ),
        migrations.CreateModel(
            name='Descriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.TextField()),
                ('points', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motion', models.CharField(max_length=64)),
                ('vote_type', models.CharField(choices=[('simple', 'simple majority'), ('2/3', '2/3 majority')], default='simple', max_length=16)),
                ('speeches', models.BooleanField(default=False)),
                ('duration', models.BooleanField(default=False)),
                ('speaking_time', models.BooleanField(default=False)),
                ('topic', models.BooleanField(default=False)),
                ('purpose', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MotionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.FloatField(default=0)),
                ('duration', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('speaking_time', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('purpose', models.CharField(blank=True, max_length=128, null=True)),
                ('delegation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.delegation')),
                ('motion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.motion')),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('max_possible', models.FloatField()),
                ('criteria', models.ManyToManyField(to='dartmun.Criterion')),
            ],
        ),
        migrations.CreateModel(
            name='TallyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('acronym', models.CharField(max_length=8)),
                ('weight', models.PositiveSmallIntegerField()),
                ('scaled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=128)),
                ('number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TallyScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('time', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.tallycategory')),
                ('delegation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.delegation')),
                ('scorer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.chair')),
            ],
        ),
        migrations.CreateModel(
            name='TallyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('acronym', models.CharField(max_length=8)),
                ('categories', models.ManyToManyField(to='dartmun.TallyCategory')),
            ],
        ),
        migrations.CreateModel(
            name='TallyCategoryScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_score', models.FloatField(default=0)),
                ('zscore', models.FloatField(blank=True, null=True)),
                ('scaled_score', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.committeetallycategory')),
                ('tallies', models.ManyToManyField(to='dartmun.TallyScore')),
            ],
        ),
        migrations.CreateModel(
            name='SpeechEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delegation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dartmun.delegation')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(blank=True, null=True)),
                ('delegation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.delegation')),
                ('tally_category_scores', models.ManyToManyField(to='dartmun.TallyCategoryScore')),
            ],
        ),
        migrations.CreateModel(
            name='RubricEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.FloatField(blank=True, null=True)),
                ('criterion_scores', models.ManyToManyField(to='dartmun.CriterionScore')),
                ('rubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.rubric')),
            ],
        ),
        migrations.AddField(
            model_name='rubric',
            name='tally_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.tallycategory'),
        ),
        migrations.CreateModel(
            name='PeopleManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simple_majority', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('super_majority', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('number_present', models.PositiveSmallIntegerField(default=0)),
                ('delegations', models.ManyToManyField(to='dartmun.Delegation')),
                ('directors', models.ManyToManyField(to='dartmun.CommitteeDirector')),
                ('managers', models.ManyToManyField(to='dartmun.CommitteeManager')),
            ],
        ),
        migrations.CreateModel(
            name='ParliProManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.BooleanField(default=False)),
                ('default_st', models.PositiveSmallIntegerField(default=120)),
                ('current_st', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('caucus_duration', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('remaining_speeches', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('current_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.debatemode')),
                ('current_topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.topic')),
                ('motion_list', models.ManyToManyField(to='dartmun.MotionEntry')),
                ('speaker_list', models.ManyToManyField(to='dartmun.SpeechEntry')),
            ],
        ),
        migrations.AddField(
            model_name='motionentry',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.topic'),
        ),
        migrations.CreateModel(
            name='GradesManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_average', models.FloatField(default=87.5)),
                ('category_stdev', models.FloatField(default=5)),
                ('need_update', models.BooleanField(default=False)),
                ('score_managers', models.ManyToManyField(to='dartmun.ScoreManager')),
                ('tallies', models.ManyToManyField(to='dartmun.TallyScore')),
                ('tally_categories', models.ManyToManyField(to='dartmun.CommitteeTallyCategory')),
            ],
        ),
        migrations.AddField(
            model_name='criterionscore',
            name='descriptor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.descriptor'),
        ),
        migrations.AddField(
            model_name='criterion',
            name='possible_scores',
            field=models.ManyToManyField(to='dartmun.Descriptor'),
        ),
        migrations.AddField(
            model_name='committeetallycategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dartmun.tallycategory'),
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('acronym', models.CharField(max_length=8)),
                ('grades', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.gradesmanager')),
                ('parli_pro', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.parlipromanager')),
                ('people', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dartmun.peoplemanager')),
                ('topics', models.ManyToManyField(to='dartmun.Topic')),
            ],
        ),
    ]
