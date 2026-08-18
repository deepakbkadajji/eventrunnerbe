from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_alter_appreleaseversiontable_releaseversionnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndConditionsTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(default='app', max_length=50)),
                ('version_number', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('effective_from', models.DateTimeField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('document_type', 'version_number')},
            },
        ),
        migrations.CreateModel(
            name='ParticipantTermsAcceptanceTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_at', models.DateTimeField(auto_now_add=True)),
                ('app_version', models.CharField(blank=True, max_length=50, null=True)),
                ('device_type', models.CharField(blank=True, max_length=100, null=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms_acceptances', to='api.participanttable')),
                ('terms', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='acceptances', to='api.termsandconditionstable')),
            ],
            options={
                'ordering': ['-accepted_at'],
                'unique_together': {('participant', 'terms')},
            },
        ),
    ]
