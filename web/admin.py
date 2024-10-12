from django.contrib import admin
from .models import Member, Event, Announcement, District, Gallery, Role, Leader, Contact, GalleryFile
from django.contrib.auth.models import User

admin.site.register(Event)
admin.site.register(Announcement)
admin.site.register(Gallery)
admin.site.register(Member)
admin.site.register(Role)
admin.site.register(Leader)
admin.site.register(Contact)
admin.site.register(GalleryFile)




class MemberInLine(admin.StackedInline):
    model = Member

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name','email']
    inlines = [MemberInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)


from django.contrib import admin
from .models import District, Member

class MemberInline(admin.TabularInline):
    model = Member
    extra = 0  # Set to 0 if you don't want extra empty forms

class DistrictAdmin(admin.ModelAdmin):
    inlines = [MemberInline]

admin.site.register(District, DistrictAdmin)
