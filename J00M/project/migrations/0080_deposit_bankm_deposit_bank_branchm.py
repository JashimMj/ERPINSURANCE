# Generated by Django 4.0 on 2022-04-11 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('project', '0079_modofpayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit_BankM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(blank=True, max_length=500, null=True)),
                ('issu_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Edits', models.CharField(blank=True, max_length=10, null=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit_Bank_BranchM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Bank_Branch', models.CharField(blank=True, max_length=300, null=True)),
                ('Bank_Branch_Address', models.CharField(blank=True, max_length=800, null=True)),
                ('Bank_Branch_Phone', models.CharField(blank=True, max_length=20, null=True)),
                ('Bank_Branch_Mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('Bank_Branch_Email', models.EmailField(blank=True, max_length=50, null=True)),
                ('issu_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Edits', models.CharField(blank=True, max_length=10, null=True)),
                ('Bank_Name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.deposit_bankm')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]