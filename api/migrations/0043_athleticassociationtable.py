import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_athleticscategorytable'),
    ]

    operations = [
        migrations.CreateModel(
            name='AthleticAssociationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('registrationnumber', models.CharField(blank=True, max_length=50, null=True)),
                ('athleticscategory', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='athleticassociation_athleticscategory', to='api.athleticscategorytable')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organisationtable',
            name='athleticassociation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='organisation_athleticassociation', to='api.athleticassociationtable'),
        ),
    ]
