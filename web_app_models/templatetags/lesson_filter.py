from django import template
from django.shortcuts import render_to_response
from django.urls import reverse
from next_prev import next_in_order

from web_app_models.models import Lesson

register = template.Library()


@register.assignment_tag()
def filter_lessons(request, obj):
    user = request.user
    if user.is_authenticated:
        user_lessons = list()
        disabled_lessons = list()
        for pos, el in enumerate(obj):
            if el in user.learned_lessons.all():
                user_lessons.append(el)
            else:
                disabled_lessons.append(el)
        if len(user_lessons) != 0 and len(disabled_lessons) != 0:
            next_obj = disabled_lessons[0]
        else:
            next_obj = obj.first()
        if len(disabled_lessons) != 0:
            disabled_lessons.remove(next_obj)
            user_lessons.append(next_obj)
        context = {
            'user_lessons': user_lessons,
            'disabled_lessons': disabled_lessons
        }
        if request.path == reverse('all_lessons'):
            return render_to_response('partials/lesson_tile.html', context).content
        else:
            return render_to_response('partials/test_tile.html', context).content


@register.assignment_tag()
def get_next_lesson(lesson):
    next_lesson = next_in_order(lesson, Lesson.objects.all(), prev=False)
    if next_lesson:
        return dict(success=True, next_lesson_name=next_lesson.name, next_lesson_slug=next_lesson.slug)
    else:
        return dict(success=False)
