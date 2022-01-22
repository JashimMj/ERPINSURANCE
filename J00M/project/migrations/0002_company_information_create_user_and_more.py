# Generated by Django 4.0 on 2021-12-23 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_information',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AddField(
            model_name='company_information',
            name='issu_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
