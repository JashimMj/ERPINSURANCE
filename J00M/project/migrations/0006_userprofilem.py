# Generated by Django 4.0 on 2021-12-26 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project', '0005_branch_infoamtion'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Phone', models.CharField(blank=True, max_length=100, null=True)),
                ('Present_Address', models.TextField(blank=True, max_length=255, null=True)),
                ('Permanant_Address', models.TextField(blank=True, max_length=255, null=True)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='User_image')),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('Email', models.CharField(blank=True, max_length=30, null=True)),
                ('Branch_code', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
