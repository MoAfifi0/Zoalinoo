# Generated by Django 4.2.1 on 2023-05-23 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
