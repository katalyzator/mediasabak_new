# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render_to_response, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from next_prev import next_in_order

from main import parameters
from web_app_models.models import *
from web_app_models.web_app_forms.forms import BooksFilterForm


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['partners'] = Partners.objects.all()
        return context


class AboutTemplateView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutTemplateView, self).get_context_data(**kwargs)
        context['about_us'] = AboutUs.objects.first()
        return context


class LessonListView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'lesson_list.html'

    def get_template_names(self):
        if self.request.path == reverse('all_lessons'):
            return ['lesson_list.html']
        else:
            return ['lesson.html']


class TestLessonListView(ListView):
    model = Lesson
    template_name = 'lesson.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super(TestLessonListView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(test__part_id=self.kwargs['id'])
        return context


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'lesson_page.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        exercises = ExerciseQuestion.objects.filter(exercise__lesson=self.object)
        context['exercise'] = exercises
        return context

    def get_template_names(self):
        if self.request.path == reverse('test_detail', kwargs={'slug': self.object.slug}):
            return ['test_page.html']
        else:
            return ['lesson_page.html']




class PartListView(ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'part_list.html'


class BooksListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books.html'

    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        form = BooksFilterForm(self.request.GET)
        context['form'] = form
        if self.request.GET:
            language_id = self.request.GET.get('language')
            try:
                context['books'] = Book.objects.filter(language=language_id)
            except:
                context['books'] = Book.objects.all()
        return context


class MediaProjectsListView(ListView):
    model = Projects
    context_object_name = 'projects'
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        context = super(MediaProjectsListView, self).get_context_data(**kwargs)
        context['slider'] = MediaProjectsSlider.objects.all()
        return context


class MediaProjectsDetailView(DetailView):
    model = Projects
    template_name = 'single-project.html'
    context_object_name = 'project'
    slug_field = 'slug'


class UserProfileUpdate(UpdateView):
    model = Users
    template_name = 'my-profile.html'
    # form_class = UserUpdateForm
    # template_name_suffix = '_user'
    # prefix = 'user'
    fields = ('first_name', 'last_name', 'gender', 'email')

    def get_success_url(self):
        url = self.request.path
        return url

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data()
        context['all_lessons'] = Lesson.objects.all()
        return context

        #
        # def get_object(self, queryset=None):
        #     return Users.objects.get(slug=self.request.GET.get('slug'))


def get_type_of_exercise_question(obj):
    question = obj
    context = {
        'question': question,
        'next_question': next_in_order(obj)
    }
    if question.type == 'default':
        return render_to_response('exercises/default_test.html', context)
    elif question.type == 'image':
        return render_to_response('exercises/image_test.html', context)
    elif question.type == 'input':
        return render_to_response('exercises/input_test.html', context)
    elif question.type == 'video':
        return render_to_response('exercises/video_test.html', context)
    elif question.type == 'juxtaposition':
        return render_to_response('exercises/juxtaposition.html', context)
    elif question.type == 'multiple':
        return render_to_response('exercises/multiple_answer_test.html', context)
    else:
        return JsonResponse(dict(success=False, message='Hey'))


def get_type_of_question(obj):
    question = obj
    context = {
        'question': question,
        'next_question': next_in_order(obj)
    }
    if question.type == 'default':
        return render_to_response('default_test.html', context)
    elif question.type == 'image':
        return render_to_response('image_test.html', context)
    elif question.type == 'input':
        return render_to_response('input_test.html', context)
    elif question.type == 'video':
        return render_to_response('video_test.html', context)
    elif question.type == 'juxtaposition':
        return render_to_response('juxtaposition.html', context)
    elif question.type == 'multiple':
        return render_to_response('multiple_answer_test.html', context)
    else:
        return JsonResponse(dict(success=False, message='Hey'))


@csrf_exempt
def get_next_exercise_question(request, question_id, exercise_id):
    current_question = ExerciseQuestion.objects.get(id=question_id)
    all_questions = ExerciseQuestion.objects.filter(exercise=exercise_id)
    next_question = next_in_order(current_question, all_questions, prev=False)
    if not request.POST.get('test'):
        if next_question:
            return get_type_of_exercise_question(next_question)
        else:
            return render_to_response('exercises/end.html')
    else:
        return get_type_of_exercise_question(current_question)


@csrf_exempt
def check_answer(request, question_id):
    if request.method == "POST":
        current_question = ExerciseQuestion.objects.get(id=question_id)
        all_correct_answers = ExerciseAnswer.objects.filter(question=question_id, is_correct=True)
        if request.POST.get('answers[]'):
            point = 0
            try:
                answers = request.POST.getlist('answers[]')
                if current_question.type == 'input':
                    if answers[0] == all_correct_answers.answer:
                        point += 1
                elif current_question.type == 'juxtaposition':
                    for i in answers:
                        if ExerciseAnswer.objects.get(id=i.split(':')[0]).true_choice == i.split(':')[1]:
                            point += 1 / all_correct_answers.count()
                elif current_question.type == 'multiple':
                    for i in answers:
                        if i != 0:
                            if ExerciseAnswer.objects.get(id=i) in all_correct_answers:
                                point = point + 1
                            else:
                                point -= 1 / all_correct_answers.count()
                else:
                    for i in answers:
                        if ExerciseAnswer.objects.get(id=i) in all_correct_answers:
                            point += 1
                if point == 1:
                    return JsonResponse(dict(success=True, message='You good'))
                else:
                    return JsonResponse(dict(success=False, message='You not good'))
            except ObjectDoesNotExist:
                pass


@csrf_exempt
def test_next_question(request, question_id, test_id):
    if request.method == "POST":
        current_question = TestQuestion.objects.get(id=question_id)
        all_correct_answers = TestAnswer.objects.filter(question=question_id, is_correct=True)
        all_questions = TestQuestion.objects.filter(test=test_id)
        user_id = request.user.pk
        user = Users.objects.get(id=user_id)
        if request.POST.get('answers[]'):
            point = request.session['point']
            try:
                answers = request.POST.getlist('answers[]')
                next_question = next_in_order(current_question, all_questions, prev=False)
                next_lesson = next_in_order(Lesson.objects.get(test__exact=test_id),
                                            Lesson.objects.filter(test__isnull=False,
                                                                  test__test_question__isnull=False), prev=False)
                if current_question.type == 'input':
                    if answers[0] == all_correct_answers.answer:
                        point += 1
                elif current_question.type == 'juxtaposition':
                    for i in answers:
                        if TestAnswer.objects.get(id=i.split(':')[0]).true_choice == i.split(':')[1]:
                            point += 1 / all_correct_answers.count()
                elif current_question.type == 'multiple':
                    for i in answers:
                        if i != 0:
                            if TestAnswer.objects.get(id=i) in all_correct_answers:
                                point += 1 / all_correct_answers.count()
                            else:
                                point -= 1 / all_correct_answers.count()
                else:
                    for i in answers:
                        if TestAnswer.objects.get(id=i) in all_correct_answers:
                            point += 1
                if next_question:
                    return_obj = get_type_of_question(next_question)
                else:
                    if next_in_order(Test.objects.get(id=test_id), Test.objects.all(), prev=False):
                        is_last = False
                    else:
                        is_last = True
                    return_obj = render_to_response('result.html',
                                                    {'point': (point / TestQuestion.objects.filter(
                                                        test=test_id).count()) * 100, 'next_lesson': next_lesson,
                                                     'is_last': is_last, 'user': user})
                    if (point / all_questions.count()) * 100 > 40:
                        user.learned_lessons.add(Test.objects.get(id=test_id).lesson)
                        result, flag = Results.objects.get_or_create(user=user, test=Test.objects.get(id=test_id))
                        result.point = point = (point / all_questions.count()) * 100
                        result.save()
                request.session['point'] = point
                return return_obj
            except ObjectDoesNotExist:
                request.session['point'] = 0
                return get_type_of_question(current_question)
        else:
            request.session['point'] = 0
            return get_type_of_question(current_question)


@login_required
def PDFTemplateView(request):
    context = {'user': request.user, 'base_url': parameters.BASE_URL}
    return render(request, 'partials/pdf.html', context)
