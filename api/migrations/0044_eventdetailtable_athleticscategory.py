import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_athleticassociationtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetailtable',
            name='athleticscategory',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name='event_athleticscategory',
                to='api.athleticscategorytable',
            ),
        ),
    ]
