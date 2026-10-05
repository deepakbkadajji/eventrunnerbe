from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_appnotificationtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantNotificationReadTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_kind', models.CharField(max_length=20)),
                ('notification_id', models.PositiveIntegerField()),
                ('read_at', models.DateTimeField(auto_now_add=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_reads', to='api.participanttable')),
            ],
            options={
                'ordering': ['-read_at'],
            },
        ),
        migrations.AddIndex(
            model_name='participantnotificationreadtable',
            index=models.Index(fields=['participant', 'notification_kind'], name='api_partici_partici_8a4f2d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='participantnotificationreadtable',
            unique_together={('participant', 'notification_kind', 'notification_id')},
        ),
    ]
