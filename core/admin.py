from django.contrib import admin

# Register your models here.
from core.models import Logging, Admin

admin.site.register(Logging)
admin.site.register(Admin)