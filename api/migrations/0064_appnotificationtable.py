import utilities.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_eventsubdetailtable_routegpx_routepolyline'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppNotificationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('notificationImg', models.ImageField(blank=True, null=True, storage=utilities.storage_backends.PrivateMediaStorage(), upload_to='images/appNotificationImg/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
