# Generated by Django 4.0.3 on 2022-03-13 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='bankaccount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
