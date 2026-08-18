from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_subscription_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('devicetype', models.CharField(blank=True, max_length=100, null=True)),
                ('error_location', models.CharField(blank=True, max_length=255, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('call_stack', models.TextField(blank=True, null=True)),
                ('http_url', models.CharField(blank=True, max_length=500, null=True)),
                ('http_status', models.IntegerField(blank=True, null=True)),
                ('http_call_req_body', models.TextField(blank=True, null=True)),
                ('input_from_user', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
