from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_errortable'),
    ]

    operations = [
        migrations.AddField(
            model_name='errortable',
            name='error_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='errortable',
            name='participant',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='error_participant',
                to='api.participanttable',
            ),
        ),
    ]
