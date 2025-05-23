# Generated by Django 5.2 on 2025-05-07 15:17

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('administrator', 'Administrator'), ('police_officer', 'Police Officer'), ('client', 'Client')], default='client', max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_legal_name', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=20)),
                ('license_status', models.CharField(choices=[('active', 'Active'), ('revoked', 'Revoked'), ('suspended', 'Suspended'), ('pending', 'Pending')], default='pending', max_length=10)),
                ('registration_date', models.DateField()),
                ('age', models.PositiveIntegerField()),
                ('residential_address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(condition=models.Q(('full_legal_name__isnull', False)), fields=('full_legal_name',), name='unique_owner_name')],
            },
        ),
        migrations.CreateModel(
            name='Firearm',
            fields=[
                ('serial_number', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('gun_model', models.CharField(max_length=255)),
                ('gun_type', models.CharField(choices=[('handgun', 'Handgun'), ('rifle', 'Rifle'), ('shotgun', 'Shotgun'), ('submachine', 'Submachine Gun'), ('other', 'Other')], max_length=20)),
                ('ammunition_type', models.CharField(max_length=100)),
                ('firearm_status', models.CharField(choices=[('deposit', 'Deposit'), ('confiscated', 'Confiscated'), ('surrendered', 'Surrendered'), ('abandoned', 'Abandoned')], max_length=20)),
                ('date_of_collection', models.DateField()),
                ('registration_location', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='firearms', to='api.owner')),
            ],
        ),
    ]
