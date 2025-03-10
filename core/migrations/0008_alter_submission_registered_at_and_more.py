# Generated by Django 5.1.6 on 2025-03-02 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_microevent_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='teamname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='teamname',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
