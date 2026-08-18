from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_athleticorganisation_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetailtable',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='maximumparticipants',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='registrationclosedate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='registrationopendate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='sanctionreference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='sanctionstatus',
            field=models.CharField(default='UNREGISTERED', max_length=20),
        ),
        migrations.AddField(
            model_name='eventdetailtable',
            name='venuename',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='distanceunit',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='distancevalue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='maximumparticipants',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventsubdetailtable',
            name='minimumage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participanteventtable',
            name='bibnumber',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='participanteventtable',
            name='registrationdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participanteventtable',
            name='registrationnumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='emergencycontactname',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='emergencycontactphone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='identitynumber',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='isactive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='isverified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='nationalitycode',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='participanttable',
            name='passportnumber',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
