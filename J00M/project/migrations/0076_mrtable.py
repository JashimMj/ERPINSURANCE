# Generated by Django 4.0 on 2022-04-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0075_covernover_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='MRTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Mrno', models.CharField(blank=True, max_length=255, null=True)),
                ('Mod', models.CharField(blank=True, max_length=255, null=True)),
                ('Cheque_no', models.CharField(blank=True, max_length=255, null=True)),
                ('Bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('Bank_address', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]