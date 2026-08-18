import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_eventdetailtable_parkinglat_parkinglng'),
    ]

    operations = [
        migrations.CreateModel(
            name='AthleticOrganisationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('organisationtype', models.IntegerField(choices=[(0, 'International'), (1, 'National'), (2, 'Regional'), (3, 'SubRegional'), (4, 'Association'), (5, 'Club')])),
                ('registrationnumber', models.CharField(blank=True, max_length=50, null=True)),
                ('countrycode', models.CharField(blank=True, max_length=10, null=True)),
                ('province', models.CharField(blank=True, max_length=50, null=True)),
                ('postcode', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('physicaladdress', models.TextField(blank=True, null=True)),
                ('contactname', models.CharField(blank=True, max_length=50, null=True)),
                ('contactsurname', models.CharField(blank=True, max_length=50, null=True)),
                ('contactemail', models.CharField(blank=True, max_length=100, null=True)),
                ('contactphone', models.CharField(blank=True, max_length=50, null=True)),
                ('websiteurl', models.CharField(blank=True, max_length=255, null=True)),
                ('isverified', models.BooleanField(default=False)),
                ('isactive', models.BooleanField(default=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/AthelicOrgLogo/')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='images/AthleticOrgBanner/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AthleticOrganisationCategoryTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isprimary', models.BooleanField(default=False)),
                ('isactive', models.BooleanField(default=True)),
                ('athleticorganisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='athleticorganisationcategory_athleticorganisation', to='api.athleticorganisationtable')),
                ('athleticscategory', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='athleticorganisationcategory_athleticscategory', to='api.athleticscategorytable')),
            ],
            options={
                'unique_together': {('athleticscategory', 'athleticorganisation')},
            },
        ),
        migrations.CreateModel(
            name='AthleticOrganisationMemberTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membershipnumber', models.CharField(blank=True, max_length=50, null=True)),
                ('membershiptype', models.CharField(blank=True, max_length=50, null=True)),
                ('role', models.IntegerField(choices=[(0, 'Member'), (1, 'Admin'), (2, 'Secretary'), (3, 'Director'), (4, 'Owner')], default=0)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive'), (2, 'Pending'), (3, 'expired'), (4, 'rejected'), (5, 'cancelled'), (6, 'suspended'), (7, 'terminated'), (8, 'onhold')], default=2)),
                ('membershipstartdate', models.DateField(blank=True, null=True)),
                ('membershipenddate', models.DateField(blank=True, null=True)),
                ('isprimary', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('athleticorganisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='athleticorganisationmember_athleticorganisation', to='api.athleticorganisationtable')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='athleticorganisationmember_participant', to='api.participanttable')),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('participant', 'athleticorganisation')},
            },
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='athleticorganisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='event_athleticorganisation', to='api.athleticorganisationtable'),
        ),
    ]
