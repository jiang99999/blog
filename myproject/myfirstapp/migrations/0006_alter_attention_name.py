# Generated by Django 3.2 on 2021-05-24 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfirstapp', '0005_alter_account_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attention',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]