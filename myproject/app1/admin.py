from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(student)
admin.site.register(admindata)
admin.site.register(employee)
admin.site.register(logindata)
admin.site.register(photodata)
admin.site.register(feesrecord)
admin.site.register(installment)