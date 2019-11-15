from django.contrib import admin

# Register your models here.

from alumnirekisteri.rekisteri.models import *


class PersonAdmin(admin.ModelAdmin):
    list_display = ("fullname", "member_until", "member_type")
    search_fields = ("fullname",)


admin.site.register(Person, PersonAdmin)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Skill)
admin.site.register(MailList)
admin.site.register(Language)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(PositionOfTrust)
admin.site.register(StudentOrganizationalActivity)
admin.site.register(Volunteer)
admin.site.register(Honor)
admin.site.register(Interest)
admin.site.register(FamilyMember)
