from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group

from web_app_models.web_app_forms.forms import *
from web_app_models.models import *


class ImagesInline(admin.StackedInline):
    model = ImageSlide
    exta = 2


class TestAnswerInline(admin.StackedInline):
    model = TestAnswer
    extra = 2


class FactsInline(admin.StackedInline):
    model = InterestingFacts
    extra = 2


class TestQuestionAdmin(admin.ModelAdmin):
    inlines = (TestAnswerInline,)


class ExerciseAnswerInline(admin.StackedInline):
    model = ExerciseAnswer
    extra = 2


class ExerciseQuestionAdmin(admin.ModelAdmin):
    list_filter = ('exercise',)
    list_display = ('name', 'exercise',)
    inlines = (ExerciseAnswerInline,)


class LessonAdmin(admin.ModelAdmin):
    inlines = (ImagesInline, FactsInline,)


class BookAdmin(admin.ModelAdmin):
    form = BooksUploadForm


admin.site.register(Users)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(ExerciseQuestion, ExerciseQuestionAdmin)
admin.site.register(Exercise)
admin.site.register(Test)
admin.site.register(Projects)
admin.site.register(MediaProjectsSlider)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Languages)
admin.site.unregister(Group)
admin.site.register(ExerciseAnswer)
admin.site.register(Results)
admin.site.register(Partners)
admin.site.register(AboutUs)
admin.site.register(Part)
admin.site.register(Question)
admin.site.register(Answer)
