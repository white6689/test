# Generated by Django 3.2.15 on 2022-10-01 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_instance_git_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='index_folder',
            field=models.CharField(max_length=100, null=True),
        ),
    ]