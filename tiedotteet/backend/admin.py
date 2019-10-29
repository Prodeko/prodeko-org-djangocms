from django.contrib import admin
from tiedotteet.backend.models import Category, MailConfiguration, Message, Tag

admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(MailConfiguration)
