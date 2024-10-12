from django.contrib import admin
from .models import Badge, BadgeTerm, GradeAttachment, BadgeGradingSystem


admin.site.register(Badge)
admin.site.register(BadgeTerm)
admin.site.register(GradeAttachment)
admin.site.register(BadgeGradingSystem)

