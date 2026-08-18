from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_appreleaseversiontable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appreleaseversiontable',
            name='releaseVersionNumber',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
