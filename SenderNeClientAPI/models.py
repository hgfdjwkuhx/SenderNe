from django.db import models

# Create your models here.


from django.db import models
from django.conf import settings
# Create your models here.
from SenderNeClientAPI.Commons import RandomIds
from django.utils.translation import ugettext as _

from SenderNeClientAPI.Commons.BlockStates import BlockedStatu




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

class PhoneDevicePrivateUserInfoManager(models.Manager):

    pass

class PhoneDevicePrivateUserInfo(models.Model):
    class DeviceState:
        Cancled = "cancled"
        Deleted = "deleted"
        JustAdd = "just_add"
        Unknown = "unknown"
        Refused = "refused"
        Available = "available"
        # WaitAccept = "wait_accept"
        # NeedRefresh = "need_refresh"

        DeviceStates_List = [
            Cancled,
            Deleted,
            JustAdd,
            Unknown,
            Refused,
            Available
        ]

        DEVICE_STATE_CHOICE = (
            (Cancled, "cancled"),
            (Deleted, "deleted"),
            (JustAdd, "just_add"),
            (Unknown, "unknown"),
            (Refused, "refused"),
            (Available, "available")
        )

    id = models.AutoField(primary_key=True)

    self_objectId = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivatePhoneDevicePrivateUser_SelfObjectId)
    client_objectId = models.CharField(max_length=100, null=True , unique=True)

    user_private_processor_objectId = models.CharField(max_length=100, null=True)
    user_private_processor = models.ForeignKey(UserPrivateProcessorInfo, related_name='related_phone_device_private_user_info',   on_delete=models.SET_NULL, null=True, blank=True)


    device_name = models.CharField(max_length=100, null=True , unique=True)
    blocked_state = models.CharField(max_length=20, choices=BlockedStatu.BLOCKED_STATUS_CHOICE, null=True,
                                                default=BlockedStatu.JustAdd)
    device_state = models.CharField(max_length=20, choices=DeviceState.DEVICE_STATE_CHOICE, null=True,
                                                default=DeviceState.JustAdd)

    temp_token = models.TextField(default=RandomIds.get_random_PrivatePhoneDevicePrivateUser_DeviceToken)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PhoneDevicePrivateUserInfoManager()

    def __str__(self):
        return str(self.user_private_processor)

    def get_InfoDic_clinet(self):
        return {
            "device_objectId" : self.client_objectId,
            "device_name": self.device_name,
            "device_state": str(self.device_state),
            "token": self.temp_token
        }

    class Meta:
        db_table = 'at_phone_device_private_user_infos'



#---------------------------: Temp :-------------------------------------------/

def get_socket_url():
    from SenderNeWebProject.settings import isLocal
    if isLocal:
        return "ws://localhost:5002/"
    else:
        return "wss://sendneserver.herokuapp.com/"


class TempUserPrivateProcessorInfoManager(models.Manager):

    pass

class TempUserPrivateProcessorInfo(models.Model):
    id = models.AutoField(primary_key=True)

    user_objectId = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivateUser_TempUserObjectId)
    user_identifier = models.CharField(max_length=100, null=True , default=RandomIds.get_random_PrivateUser_TempUserIdentifier)

    processor_info = models.ForeignKey(ProcessorInfo, related_name='related_temp_user_private_processor_info',   on_delete=models.SET_NULL, null=True, blank=True)

    blocked_state = models.CharField(max_length=20, choices=BlockedStatu.BLOCKED_STATUS_CHOICE, null=True,
                                                default=BlockedStatu.JustAdd)

    temp_token = models.TextField(default=RandomIds.get_random_PrivateTempUser_TempUserToken)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TempUserPrivateProcessorInfoManager()

    def __str__(self):
        return str(self.user_objectId)

    def resultt_new(self):
        return {
            "identifier" : self.user_identifier
        }
    def get_tokenInfo(self):
        return {
            "temp_token" : self.temp_token,
            "socket_uri" : get_socket_url()
        }

    class Meta:
        db_table = 'at_temp_user_private_processor_infos'


#---------------------------: Temp Socket Phone :-------------------------------------------/

class TempPhoneDevicePrivateUserInfoManager(models.Manager):

    pass

class TempPhoneDevicePrivateUserInfo(models.Model):
    class DeviceState:
        Cancled = "cancled"
        Deleted = "deleted"
        JustAdd = "just_add"
        Unknown = "unknown"
        Refused = "refused"
        Available = "available"
        # WaitAccept = "wait_accept"
        # NeedRefresh = "need_refresh"

        DeviceStates_List = [
            Cancled,
            Deleted,
            JustAdd,
            Unknown,
            Refused,
            Available
        ]

        DEVICE_STATE_CHOICE = (
            (Cancled, "cancled"),
            (Deleted, "deleted"),
            (JustAdd, "just_add"),
            (Unknown, "unknown"),
            (Refused, "refused"),
            (Available, "available")
        )

    id = models.AutoField(primary_key=True)

    self_objectId = models.CharField(max_length=100, null=True , default=RandomIds.get_random_TempPrivatePhoneDevicePrivateUser_SelfObjectId)
    client_objectId = models.CharField(max_length=100, null=True , unique=True)

    temp_user_private_processor_objectId = models.CharField(max_length=100, null=True)
    temp_user_private_processor = models.ForeignKey(TempUserPrivateProcessorInfo, related_name='related_temp_phone_device_private_user_info',   on_delete=models.SET_NULL, null=True, blank=True)


    device_name = models.CharField(max_length=100, null=True , unique=True)
    blocked_state = models.CharField(max_length=20, choices=BlockedStatu.BLOCKED_STATUS_CHOICE, null=True,
                                                default=BlockedStatu.JustAdd)
    device_state = models.CharField(max_length=20, choices=DeviceState.DEVICE_STATE_CHOICE, null=True,
                                                default=DeviceState.JustAdd)

    temp_token = models.TextField(default=RandomIds.get_random_TempPrivatePhoneDevicePrivateUser_DeviceToken)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TempPhoneDevicePrivateUserInfoManager()

    def __str__(self):
        return str(self.temp_user_private_processor)

    def get_InfoDic_clinet(self):
        return {
            "device_objectId" : self.client_objectId,
            "device_name": self.device_name,
            "device_state": str(self.device_state),
            "token": self.temp_token
        }

    class Meta:
        db_table = 'at_temp_phone_device_private_user_infos'














