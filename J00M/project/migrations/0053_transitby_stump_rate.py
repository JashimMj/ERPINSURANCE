# Generated by Django 4.0 on 2022-03-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0052_remove_transitby_stump_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='transitby',
            name='Stump_Rate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]