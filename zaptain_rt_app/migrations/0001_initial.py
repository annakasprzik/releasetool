# Generated by Django 2.0.9 on 2018-10-08 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import zaptain_rt_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('external_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('has_abstract', models.BooleanField(default=False)),
                ('doc_type', models.CharField(blank=True, max_length=50)),
                ('broader', models.ManyToManyField(blank=True, related_name='narrower', to='zaptain_rt_app.Document')),
            ],
            options={
                'ordering': ('external_id',),
            },
        ),
        migrations.CreateModel(
            name='Guideline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('description', models.CharField(blank=True, max_length=500)),
                ('link', zaptain_rt_app.models.PermissiveUrlField(blank=True)),
            ],
            options={
                'get_latest_by': 'pub_date',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ReleaseCandidate',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('pub_date', models.DateTimeField(help_text='Published means, e.g., upload into releasetool, not published to operative IR system.', verbose_name='date published')),
                ('file', models.FileField(help_text='File content:\n        tab-separated values; for each row: first cell = document external id, then subjects', upload_to='releasecandidates/')),
                ('concept_template', models.CharField(blank=True, help_text='str.format template with concept id inserted as named argument "cid", e.g., http://zbw.eu/stw/descriptor/{cid}', max_length=300, null=True)),
            ],
            options={
                'get_latest_by': 'pub_date',
                'ordering': ('pub_date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_rating', models.CharField(choices=[('skip', 'skip'), ('reject', 'reject'), ('fair', 'fair'), ('good', 'good')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RtConfig',
            fields=[
                ('key', models.CharField(choices=[('main_ai', 'name of the main automatic indexing method'), ('support_email', 'support email'), ('catalog_api_pattern', 'catalog API pattern'), ('document_weblink_pattern', 'document weblink pattern'), ('thesaurus_descriptor_type', 'thesaurus descriptor type'), ('thesaurus_category_type', 'thesaurus category type'), ('thesaurus_sparql_endpoint', 'thesaurus sparql endpoint'), ('thesaurus_sparql_query', 'thesaurus sparql query')], max_length=50, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('key',),
            },
        ),
        migrations.CreateModel(
            name='SubjectAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.URLField(max_length=300)),
                ('score', models.DecimalField(decimal_places=2, max_digits=3)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.Document')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectIndexer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ai_name', models.CharField(max_length=500)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectLevelReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('harmful', 'harmful'), ('fair', 'fair'), ('helpful', 'helpful'), ('reallyhelpful', 'really helpful')], max_length=20)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.Review')),
                ('subject_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.SubjectAssignment')),
            ],
        ),
        migrations.AddField(
            model_name='subjectassignment',
            name='indexer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.SubjectIndexer'),
        ),
        migrations.AddField(
            model_name='subjectassignment',
            name='review_binding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='missing_subjects', to='zaptain_rt_app.Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='ai',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.SubjectIndexer'),
        ),
        migrations.AddField(
            model_name='review',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.Document'),
        ),
        migrations.AddField(
            model_name='review',
            name='guideline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.Guideline'),
        ),
        migrations.AddField(
            model_name='review',
            name='ratings',
            field=models.ManyToManyField(through='zaptain_rt_app.SubjectLevelReview', to='zaptain_rt_app.SubjectAssignment'),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='releasecandidate',
            name='indexer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaptain_rt_app.SubjectIndexer'),
        ),
        migrations.AddField(
            model_name='collection',
            name='documents',
            field=models.ManyToManyField(to='zaptain_rt_app.Document'),
        ),
        migrations.AlterUniqueTogether(
            name='subjectlevelreview',
            unique_together={('review', 'subject_assignment')},
        ),
        migrations.AlterUniqueTogether(
            name='subjectassignment',
            unique_together={('document', 'subject', 'indexer')},
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('reviewer', 'document', 'ai')},
        ),
    ]
