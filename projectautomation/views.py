from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from .forms import ChooseTimeForm
from .models import Student

ERRORS = [
    'Все группы заняты.',
    'Этот временной слот уже скомплектован.',
    'Может еще какая ошибка ))'
]


def show_time_slots(request, proj_id, user_id, error_id=None):
    try:
        student = Student.objects.get(id=user_id)
    except Student.DoesNotExist:
        raise Http404('Page Not Found')
    else:
        if request.method == 'POST':
            form = ChooseTimeForm(request.POST)
            if form.is_valid():
                best_time_slots = form.cleaned_data.get('best_time_slots')

                student.best_time_slots.set(best_time_slots)

                return HttpResponseRedirect('/thanks/')

        form = ChooseTimeForm()
        context = {'proj_id': proj_id,
                   'user_id': user_id,
                   'form': form,
                   'name': student.first_name}

        if error_id:
            context['error'] = ERRORS[error_id - 1]

        return render(request, 'index.html', context=context)


def show_thanks(request):
    return render(request, 'thanks.html')
