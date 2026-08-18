import utilities.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_merge_20260808_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnotificationtable',
            name='notificationPdf',
            field=models.FileField(
                blank=True,
                null=True,
                storage=utilities.storage_backends.PrivateMediaStorage(),
                upload_to='files/notificationPdf/',
            ),
        ),
    ]
