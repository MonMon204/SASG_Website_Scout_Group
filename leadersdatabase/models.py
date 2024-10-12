from django.db import models
from web.models import District

class resource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=100, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    
class resources_files(models.Model):
    resource = models.ForeignKey(resource, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources_files/', blank=True)

    def __str__(self):
        return self.file.name
    
class camp_sites(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=100, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    
class camp_sites_files(models.Model):
    camp_site = models.ForeignKey(camp_sites, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='camp_sites_files/', blank=True)

    def __str__(self):
        return self.file.name