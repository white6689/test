# Generated by Django 3.2.15 on 2022-10-01 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20220930_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='git_commit',
            field=models.CharField(max_length=30, null=True),
        ),
    ]