# Generated by Django 4.0 on 2022-04-04 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0072_alter_marinecovernotem_sum_insured_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marinecovernotem',
            name='Cover_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]