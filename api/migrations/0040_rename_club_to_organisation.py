# Generated manually for Club -> Organisation rename

import api.util
import django.db.models.deletion
import utilities.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_clubtable_clubmembertable_clubeventtable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ClubTable',
            new_name='OrganisationTable',
        ),
        migrations.RenameModel(
            old_name='ClubMemberTable',
            new_name='OrganisationMemberTable',
        ),
        migrations.RenameModel(
            old_name='ClubEventTable',
            new_name='OrganisationEventTable',
        ),
        migrations.RenameField(
            model_name='organisationmembertable',
            old_name='club',
            new_name='organisation',
        ),
        migrations.RenameField(
            model_name='organisationeventtable',
            old_name='club',
            new_name='organisation',
        ),
        migrations.AlterUniqueTogether(
            name='organisationmembertable',
            unique_together={('organisation', 'participant')},
        ),
        migrations.AlterUniqueTogether(
            name='organisationeventtable',
            unique_together={('organisation', 'event')},
        ),
        migrations.AlterField(
            model_name='organisationtable',
            name='logo',
            field=models.ImageField(
                blank=True,
                null=True,
                storage=utilities.storage_backends.PrivateMediaStorage(),
                upload_to='images/organisationLogo/',
            ),
        ),
        migrations.AlterField(
            model_name='organisationtable',
            name='banner',
            field=models.ImageField(
                blank=True,
                null=True,
                storage=utilities.storage_backends.PrivateMediaStorage(),
                upload_to='images/organisationBanner/',
            ),
        ),
        migrations.AlterField(
            model_name='organisationtable',
            name='status',
            field=models.IntegerField(
                choices=[(0, 'Active'), (1, 'Inactive')],
                default=api.util.OrganisationStatus['Active'],
            ),
        ),
        migrations.AlterField(
            model_name='organisationmembertable',
            name='status',
            field=models.IntegerField(
                choices=[(0, 'Active'), (1, 'Inactive'), (2, 'Pending')],
                default=api.util.OrganisationMemberStatus['Pending'],
            ),
        ),
        migrations.AlterField(
            model_name='organisationmembertable',
            name='role',
            field=models.IntegerField(
                choices=[
                    (0, 'Member'), (1, 'Admin'), (2, 'Secretary'),
                    (3, 'Director'), (4, 'Owner'),
                ],
                default=api.util.OrganisationMemberRole['Member'],
            ),
        ),
    ]
