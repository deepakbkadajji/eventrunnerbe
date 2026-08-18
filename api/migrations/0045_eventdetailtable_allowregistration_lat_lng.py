from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_eventdetailtable_athleticscategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetailtable',
            name='allowregistration',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True),
        ),
    ]
