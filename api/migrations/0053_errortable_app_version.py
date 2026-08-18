from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_errortable_error_method_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='errortable',
            name='app_version',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
