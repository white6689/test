# Generated by Django 3.2.15 on 2022-09-30 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_instance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='page_name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]