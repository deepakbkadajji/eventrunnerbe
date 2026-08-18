import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_eventnotificationtable_notificationpdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnotificationtable',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='eventnotificationtable',
            options={'ordering': ['-created']},
        ),
    ]
