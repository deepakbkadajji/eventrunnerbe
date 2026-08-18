from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_participant_event_subevent_detail_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlanTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plancode', models.CharField(max_length=30, unique=True)),
                ('planname', models.CharField(max_length=100)),
                ('subscribertype', models.IntegerField(choices=[(0, 'Participant'), (1, 'Organisation')])),
                ('billingfrequency', models.IntegerField(choices=[(0, 'Monthly'), (1, 'Annual'), (2, 'OnceOff')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currencycode', models.CharField(default='ZAR', max_length=3)),
                ('maximummembers', models.IntegerField(blank=True, null=True)),
                ('maximumevents', models.IntegerField(blank=True, null=True)),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriptionstartdate', models.DateField()),
                ('subscriptionenddate', models.DateField(blank=True, null=True)),
                ('nextbillingdate', models.DateField(blank=True, null=True)),
                ('subscriptionstatus', models.IntegerField(choices=[(0, 'Pending'), (1, 'Trial'), (2, 'Active'), (3, 'Suspended'), (4, 'Expired'), (5, 'Cancelled')], default=0)),
                ('autorenew', models.BooleanField(default=False)),
                ('externalcustomerid', models.CharField(blank=True, max_length=100, null=True)),
                ('externalpaymentid', models.CharField(blank=True, max_length=100, null=True)),
                ('athleticorganisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_athleticorganisation', to='api.athleticorganisationtable')),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_participant', to='api.participanttable')),
                ('subscriptionplan', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='subscription_plan', to='api.subscriptionplantable')),
            ],
        ),
    ]
