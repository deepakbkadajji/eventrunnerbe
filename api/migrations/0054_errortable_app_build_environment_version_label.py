from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_errortable_app_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='errortable',
            name='app_build',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='errortable',
            name='app_environment',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='errortable',
            name='app_version_label',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
