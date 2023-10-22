from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Group, PM, Project, Student, TimeSlot


def show_time_slots(request, project_id, user_id, error_id=None):
    student = get_object_or_404(Student, id=user_id)
    project = get_object_or_404(Project, id=project_id)
    in_group = Group.objects.filter(project_id=project, students=student)
    if in_group:
        return HttpResponseRedirect('/thanks/')
    if request.method == 'POST':
        time_slot_id = request.POST.get('best_time_slots')
        time_slot = get_object_or_404(TimeSlot, id=time_slot_id)
        pm = get_object_or_404(PM, time_slots=time_slot_id)

        group, created = Group.objects.get_or_create(
            time_slot=time_slot,
            project=project,
            defaults={
                'title': f'{project.title} - {time_slot.start_time}',
                'description': project.description,
                'pm': pm,
            }
        )
        group.students.add(student)

        return redirect('/thanks/')

    unavailable_slots = Group.objects.filter(is_complete=True)\
        .values_list('time_slot_id', flat=True)
    available_slots = PM.objects.values_list('time_slots', flat=True)
    time_slots = TimeSlot.objects.filter(id__in=available_slots) \
        .exclude(id__in=unavailable_slots).values('id', 'start_time')

    return render(request, 'index.html',
                  context={
                      'user_id': user_id,
                      'project_id': project_id,
                      'available_slots': time_slots,
                      'name': student.first_name
                  })


def show_thanks(request):
    return render(request, 'thanks.html')
