from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_eventdetailtable_allowregistration_lat_lng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventdetailtable',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='eventdetailtable',
            name='lng',
        ),
    ]
