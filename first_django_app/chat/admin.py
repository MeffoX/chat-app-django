from django.contrib import admin
from .models import Chat, Message

class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'created_at', 'author', 'text', 'receiver')
    list_display = ('text', 'created_at', 'author', 'receiver')
    search_fields = ('text',)

# Register your models here.

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)