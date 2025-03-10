# Generated by Django 5.1.6 on 2025-03-08 01:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_microevent_ad_btn_text'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='attendancemoderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='teamname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
