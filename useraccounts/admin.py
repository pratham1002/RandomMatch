from django.contrib import admin
from .models import SiteUser, Places, Sitesettings

# Register your models here.

admin.site.register(SiteUser)
admin.site.register(Places)
admin.site.register(Sitesettings)