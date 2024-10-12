from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class District(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True, related_name='members')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateField(User, auto_now=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    dads_name = models.CharField(max_length=100, blank=True)
    moms_name = models.CharField(max_length=100, blank=True)
    dads_phone = models.CharField(max_length=100, blank=True)
    moms_phone = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Automatically make the user a superuser if district is 'المجموعة' and role is 'قائد'
        if self.district and self.role:
            if self.district.name == 'المجموعة' and self.role.name == 'قائد':
                self.user.is_superuser = True
                self.user.is_staff = True
            else:
                self.user.is_superuser = False
                self.user.is_staff = False
        self.user.save()
        super().save(*args, **kwargs)

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Member(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)
        user_profile.save()

post_save.connect(create_profile, sender=User)
    

class Leader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='event_images', blank=True)
    display_on_home = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='announcement_images', blank=True)
    display_on_home = models.BooleanField(default=False)

    def __str__(self):
        return self.title


from django.db import models

class Gallery(models.Model):
    title = models.CharField(max_length=100, blank=True)
    date = models.DateField(auto_now=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Galleries'


class GalleryFile(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='gallery_files/', blank=True)
    file_type = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        # Determine file type (image, video, etc.) based on file extension
        if self.file.name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico', '.webp')):
            self.file_type = 'image'
        elif self.file.name.endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm')):
            self.file_type = 'video'
        else:
            self.file_type = 'other'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.file.name} ({self.file_type})'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
    