from django.contrib import admin

from .models import Group, Levels, PM, Project, Student, TimeSlot


@admin.register(PM)
class PMAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'level')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_at', 'level')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'project', 'time_slot', 'pm', 'trello_url', 'telegram_chat_id', 'is_complete'
    )


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('id',)
