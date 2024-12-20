# Generated by Django 4.2.16 on 2024-11-19 21:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('log_type', models.CharField(choices=[('INFO', 'Info'), ('ERROR', 'Error')], max_length=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
