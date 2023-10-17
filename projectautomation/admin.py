from django.contrib import admin

from .models import Group, PM, SendDate, Student, TimeSlot


@admin.register(PM)
class PMAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_time_slots')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
    'first_name', 'last_name', 'link_sent', 'result_sent', 'level', 'get_best_time_slots', 'get_ok_time_slots')
    list_editable = ['link_sent', 'result_sent']


@admin.register(SendDate)
class SendDateAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at')
    readonly_fields = ['title']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('timeslot',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pm', 'time_slot')
