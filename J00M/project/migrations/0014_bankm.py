# Generated by Django 4.0 on 2021-12-29 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project', '0013_designationm'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(blank=True, max_length=500, null=True)),
                ('issu_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Edits', models.CharField(blank=True, max_length=10, null=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
