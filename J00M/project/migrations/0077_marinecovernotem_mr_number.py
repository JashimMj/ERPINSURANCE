# Generated by Django 4.0 on 2022-04-11 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0076_mrtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='marinecovernotem',
            name='MR_Number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.mrtable'),
        ),
    ]