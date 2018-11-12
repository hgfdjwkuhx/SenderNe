from django.db import models
from django.conf import settings
# Create your models here.
from SenderNeClientAPI.Commons import RandomIds
from django.utils.translation import ugettext as _

from SenderNeClientAPI.Commons.BlockStates import BlockedStatu


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        """A string representation of the model."""
        return self.title


class UserPrivateStoreInfoManager(models.Manager):

    pass

class UserPrivateStoreInfo(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("store owner"), related_name="related_user_private_store_info", on_delete=models.PROTECT)

    db_name = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivateUserStore_dbName)
    store_name = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivateUserStore_storeName)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserPrivateStoreInfoManager()

    def __str__(self):
        return str(self.owner)

    class Meta:
        db_table = 'at_user_private_store_infos'


#-------------------------------------------------------------------------------/

class ProcessorInfoManager(models.Manager):

    pass

class ProcessorInfo(models.Model):
    id = models.AutoField(primary_key=True)
    processor_ObjectId = models.CharField(max_length=100, null=True,
                                          default=RandomIds.get_random_PrivateProcessor_processorObjectId , editable=False)

    processor_name = models.CharField(max_length=100, null=True, blank=False)

    processor_token = models.TextField( default=RandomIds.get_random_PrivateProcessor_processorToken , blank=False )

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProcessorInfoManager()

    def __str__(self):
        return str(self.processor_name)

    class Meta:
        db_table = 'at_processor_infos'


class UserPrivateProcessorInfoManager(models.Manager):

    pass

class UserPrivateProcessorInfo(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("store owner"), related_name="related_user_private_processor_info", on_delete=models.PROTECT)

    user_objectId = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivateUser_userObjectId)

    processor_info = models.ForeignKey(ProcessorInfo, related_name='related_user_private_processor_info',   on_delete=models.SET_NULL, null=True, blank=True)

    blocked_state = models.CharField(max_length=20, choices=BlockedStatu.BLOCKED_STATUS_CHOICE, null=True,
                                                default=BlockedStatu.JustAdd)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserPrivateProcessorInfoManager()

    def __str__(self):
        return str(self.owner)

    class Meta:
        db_table = 'at_user_private_processor_infos'


#---------------------------: Temp :-------------------------------------------/

class TempUserPrivateProcessorInfoManager(models.Manager):

    pass

class TempUserPrivateProcessorInfo(models.Model):
    id = models.AutoField(primary_key=True)

    user_objectId = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivateUser_TempUserObjectId)

    processor_info = models.ForeignKey(ProcessorInfo, related_name='related_temp_user_private_processor_info',   on_delete=models.SET_NULL, null=True, blank=True)

    blocked_state = models.CharField(max_length=20, choices=BlockedStatu.BLOCKED_STATUS_CHOICE, null=True,
                                                default=BlockedStatu.JustAdd)

    temp_token = models.TextField(default=RandomIds.get_random_PrivateTempUser_TempUserToken)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TempUserPrivateProcessorInfoManager()

    def __str__(self):
        return str(self.user_objectId)

    class Meta:
        db_table = 'at_temp_user_private_processor_infos'






