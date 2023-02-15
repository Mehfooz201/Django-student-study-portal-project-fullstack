from django.contrib import admin
from .models import *

# Register your models here.

#Notes
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']

admin.site.register(Note, NoteAdmin)


#Homework
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['subject', 'title',  'is_finished', 'user']

admin.site.register(Homework, HomeworkAdmin)


#Todo
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title',  'is_finished', 'user']

admin.site.register(Todo, TodoAdmin)