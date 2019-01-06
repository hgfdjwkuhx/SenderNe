# Generated by Django 2.0.8 on 2018-12-26 19:37

import SenderNeClientAPI.Commons.RandomIds
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneDevicePrivateUserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('self_objectId', models.CharField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivatePhoneDevicePrivateUser_SelfObjectId, max_length=100, null=True)),
                ('client_objectId', models.CharField(max_length=100, null=True, unique=True)),
                ('user_private_processor_objectId', models.CharField(max_length=100, null=True)),
                ('device_name', models.CharField(max_length=100, null=True, unique=True)),
                ('blocked_state', models.CharField(choices=[('blocked', 'blocked'), ('just_add', 'just_add'), ('running', 'running'), ('unknown', 'unknown')], default='just_add', max_length=20, null=True)),
                ('device_state', models.CharField(choices=[('cancled', 'cancled'), ('deleted', 'deleted'), ('just_add', 'just_add'), ('unknown', 'unknown'), ('refused', 'refused'), ('available', 'available')], default='just_add', max_length=20, null=True)),
                ('temp_token', models.TextField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivatePhoneDevicePrivateUser_DeviceToken)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'at_phone_device_private_user_infos',
            },
        ),
        migrations.CreateModel(
            name='ProcessorInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('processor_ObjectId', models.CharField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateProcessor_processorObjectId, editable=False, max_length=100, null=True)),
                ('processor_name', models.CharField(max_length=100, null=True)),
                ('processor_token', models.TextField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateProcessor_processorToken)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'at_processor_infos',
            },
        ),
        migrations.CreateModel(
            name='TempPhoneDevicePrivateUserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('self_objectId', models.CharField(default=SenderNeClientAPI.Commons.RandomIds.get_random_TempPrivatePhoneDevicePrivateUser_SelfObjectId, max_length=100, null=True)),
                ('client_objectId', models.CharField(max_length=100, null=True, unique=True)),
                ('temp_user_private_processor_objectId', models.CharField(max_length=100, null=True)),
                ('device_name', models.CharField(max_length=100, null=True, unique=True)),
                ('blocked_state', models.CharField(choices=[('blocked', 'blocked'), ('just_add', 'just_add'), ('running', 'running'), ('unknown', 'unknown')], default='just_add', max_length=20, null=True)),
                ('device_state', models.CharField(choices=[('cancled', 'cancled'), ('deleted', 'deleted'), ('just_add', 'just_add'), ('unknown', 'unknown'), ('refused', 'refused'), ('available', 'available')], default='just_add', max_length=20, null=True)),
                ('temp_token', models.TextField(default=SenderNeClientAPI.Commons.RandomIds.get_random_TempPrivatePhoneDevicePrivateUser_DeviceToken)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'at_temp_phone_device_private_user_infos',
            },
        ),
        migrations.CreateModel(
            name='TempUserPrivateProcessorInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_objectId', models.CharField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateUser_TempUserObjectId, max_length=100, null=True)),
                ('user_identifier', models.CharField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateUser_TempUserIdentifier, max_length=100, null=True)),
                ('blocked_state', models.CharField(choices=[('blocked', 'blocked'), ('just_add', 'just_add'), ('running', 'running'), ('unknown', 'unknown')], default='just_add', max_length=20, null=True)),
                ('temp_token', models.TextField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateTempUser_TempUserToken)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('processor_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_temp_user_private_processor_info', to='SenderNeClientAPI.ProcessorInfo')),
            ],
            options={
                'db_table': 'at_temp_user_private_processor_infos',
            },
        ),
        migrations.CreateModel(
            name='UserPrivateProcessorInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_objectId', models.CharField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateUser_userObjectId, max_length=100, null=True)),
                ('blocked_state', models.CharField(choices=[('blocked', 'blocked'), ('just_add', 'just_add'), ('running', 'running'), ('unknown', 'unknown')], default='just_add', max_length=20, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='related_user_private_processor_info', to=settings.AUTH_USER_MODEL, verbose_name='store owner')),
                ('processor_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_user_private_processor_info', to='SenderNeClientAPI.ProcessorInfo')),
            ],
            options={
                'db_table': 'at_user_private_processor_infos',
            },
        ),
        migrations.AddField(
            model_name='tempphonedeviceprivateuserinfo',
            name='temp_user_private_processor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_temp_phone_device_private_user_info', to='SenderNeClientAPI.TempUserPrivateProcessorInfo'),
        ),
        migrations.AddField(
            model_name='phonedeviceprivateuserinfo',
            name='user_private_processor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_phone_device_private_user_info', to='SenderNeClientAPI.UserPrivateProcessorInfo'),
        ),
    ]
