from django.contrib import admin
from .models import resource, resources_files, camp_sites, camp_sites_files

admin.site.register(resource)
admin.site.register(resources_files)
admin.site.register(camp_sites)
admin.site.register(camp_sites_files)
