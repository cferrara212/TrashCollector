# Generated by Django 3.2.5 on 2021-10-25 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=5)),
                ('weekly_pickup', models.CharField(max_length=9)),
                ('one_time_pickup', models.DateField(blank=True, null=True)),
                ('suspend_start', models.DateField(blank=True, null=True)),
                ('suspend_end', models.DateField(blank=True, null=True)),
                ('date_of_last_pickup', models.DateField(blank=True, null=True)),
                ('balance', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
