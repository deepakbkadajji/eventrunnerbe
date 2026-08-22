from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_organisationnotificationtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationnotificationtable',
            name='event',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='organisationnotification_event',
                to='api.eventdetailtable',
            ),
        ),
    ]
