import utilities.storage_backends
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_terms_and_acceptance_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationNotificationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('notificationImg', models.ImageField(blank=True, null=True, storage=utilities.storage_backends.PrivateMediaStorage(), upload_to='images/organisationNotificationImg/')),
                ('notification_audience', models.IntegerField(choices=[(0, 'OrganisationMembersOnly'), (1, 'Everyone')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('athleticorganisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisationnotification_athleticorganisation', to='api.athleticorganisationtable')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
