from django.db import models
from ckeditor.fields import RichTextField
from web.models import Member


# el sharat 

# Badge Model
class Badge(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(null=True)
    image = models.ImageField(upload_to='badge_images')
    
    def __str__(self):
        return self.title

# BadgeTerm Model
class BadgeTerm(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='terms')
    term = models.TextField(blank=True)  # Term name
    description = models.TextField(blank=True)  # Explanation of the term
    grade = models.TextField(blank=True)  # Grading system explanation

    def __str__(self):
        return f'{self.term} for {self.badge.title}'

# GradeAttachment Model
class GradeAttachment(models.Model):
    badge_term = models.ForeignKey(BadgeTerm, on_delete=models.CASCADE, related_name='attachments')
    grade = models.CharField(max_length=255)  # Grade
    file = models.FileField(upload_to='grade_attachments/', blank=True)  # File attachment for each term
    description = models.TextField(blank=True)  # Optional description for each file

    def __str__(self):
        return f'Attachment for {self.badge_term.term}'


class BadgeGradingSystem(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='grading_system', null=True, blank=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='grading_system', null=True, blank=True)
    badge_term = models.ForeignKey(BadgeTerm, on_delete=models.CASCADE, related_name='grading_system', null=True, blank=True)
    grade_attachment = models.OneToOneField(GradeAttachment, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    passed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.member.user.username} - {self.badge.title} - {self.badge_term.term}'


class BadgeApproval(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='badge_approval', null=True, blank=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='badge_approval', null=True, blank=True) 
    passed = models.BooleanField(default=False)
    display_on_his_account = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.member.user.username} - {self.badge.title}'
