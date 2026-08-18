from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_remove_eventdetailtable_lat_lng'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetailtable',
            name='parkinglat',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='parkinglng',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True),
        ),
    ]
