import django.db.models.deletion
import utilities.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_organisationnotificationtable_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='routeGpx',
            field=models.FileField(
                blank=True,
                null=True,
                storage=utilities.storage_backends.PrivateMediaStorage(),
                upload_to='files/subeventRouteGpx/',
            ),
        ),
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='routePolyline',
            field=models.TextField(blank=True, null=True),
        ),
    ]
