from django.contrib import admin

# Register your models here.


from SenderNeClientAPI import models


admin.site.register(models.ProcessorInfo)
admin.site.register(models.UserPrivateProcessorInfo)
admin.site.register(models.TempUserPrivateProcessorInfo)





