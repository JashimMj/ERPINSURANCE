# Generated by Django 4.0 on 2022-01-09 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project', '0021_delete_module_name_remove_userprofilem_branch_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='software_permittion_branch',
            name='Software_Permition',
        ),
        migrations.CreateModel(
            name='Software_Permittion_Module',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Software_Permition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.software_permittion_mainm')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
