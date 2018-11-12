from django.contrib import admin

# Register your models here.


from .models import Todo , UserPrivateStoreInfo
from SenderNeClientAPI import models

admin.site.register(Todo)

admin.site.register(UserPrivateStoreInfo)
admin.site.register(models.ProcessorInfo)
admin.site.register(models.UserPrivateProcessorInfo)
admin.site.register(models.TempUserPrivateProcessorInfo)





