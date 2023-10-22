from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .forms import ChooseTimeForm
from .models import Student, Project, Group, PM, TimeSlot


def show_time_slots(request, project_id, user_id):
    try:
        student = Student.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
    except Student.DoesNotExist or Project.DoesNotExist:
        raise Http404('Page Not Found')
    else:
        if request.method == 'POST':
            print('request.POST', request.POST)
            form = ChooseTimeForm(request.POST)
            print(form.fields)
            print(form.errors)
            if form.is_valid():
                best_time_slots = form.cleaned_data.get('best_time_slots')
                group = Group.objects.get(time_slot_id=best_time_slots)
                print('find_group', group)
                if group:
                    group.students.add(student)
                else:
                    Group.objects.create(student)
                return HttpResponseRedirect('/thanks/')

        time_slots = TimeSlot.objects.all()
        best_time_slots = Group.objects.filter(is_complete=1).values("time_slot_id")
        unavailable_slots = []
        for slots in best_time_slots:
            unavailable_slots.append(slots['time_slot_id'])
        time_slots = TimeSlot.objects.exclude(id__in=unavailable_slots)
        return render(request, 'index.html',
                      context={
                          'user_id': user_id,
                          'project_id': project_id,
                          'available_slots': time_slots,
                          'name': student.first_name
                      })


def show_thanks(request):
    return render(request, 'thanks.html')