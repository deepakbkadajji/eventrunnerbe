from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_eventnotificationtable_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppReleaseVersionTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('releaseVersionNumber', models.CharField(max_length=50)),
                ('optionUpgradeVersionNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('mandatoryUpgradeVersionNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
