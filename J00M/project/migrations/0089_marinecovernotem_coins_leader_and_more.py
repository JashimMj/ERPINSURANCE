# Generated by Django 4.0 on 2022-04-19 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0088_mrtable_service_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='marinecovernotem',
            name='Coins_Leader',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='marinecovernotem',
            name='Coins_Leader_Doc',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='marinecovernotem',
            name='Coins_Leader_Name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='marinecovernotem',
            name='Coins_Leader_Persent',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='marinecovernotem',
            name='Coins_None_Leader',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
