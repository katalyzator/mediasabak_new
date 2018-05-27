from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
# Create your models here.
from django.db.models import Avg
from pytils.translit import slugify
from sorl.thumbnail import get_thumbnail

from .helpers import *


# Create your models


class Users(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    username = models.CharField(verbose_name='Логин', null=True, blank=True, max_length=255)
    gender = models.CharField(choices=(('male', 'Мужчина'), ('female', 'Женщина'),), default='male', verbose_name='Пол',
                              max_length=255, null=True, blank=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=255, blank=True)
    learned_lessons = models.ManyToManyField("Lesson", verbose_name='Пройденные тесты', blank=True)
    slug = models.SlugField(null=True, blank=True)
    REQUIRED_FIELDS = ['username', ]
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Users, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.username + '_' + str(self.pk))
        super(Users, self).save(*args, **kwargs)

    def get_point(self):
        return self.results.all().aggregate(Avg('point'))

    def get_date(self):
        return self.results.last().date

    @property
    def is_correct(self):
        if None not in [self.first_name, self.last_name, self.gender, self.email]:
            return True
        return False

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


TEST_TYPE_CHOICE = (
    ('default', 'Стандартный'),
    ('video', 'Видео'),
    ('input', 'Текстовый'),
    ('image', 'Тест с картинками'),
    ('juxtaposition', 'Сопоставление'),
    ('multiple', 'Несколько вариантов ответа'),
    # ('assessment_of', 'Оценка'),
)


class Lesson(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    image = models.ImageField(verbose_name='Превью', null=True, upload_to=transform('lesson_preview/'))
    video_key = models.CharField(verbose_name='Ключ видео на ютубе для мультфильма', max_length=255,
                                 help_text='Ключ видео после "v=" (Например https://www.youtube.com/watch?v=JGwWNGJdvx8&index=2&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbAVMG2fOum_KWQU здесь ключем будет "JGwWNGJdvx8" )',
                                 null=True)
    infographic_video_key = models.CharField(verbose_name='Ключ видео на ютубе для инфографики', max_length=255,
                                             blank=True, null=True,
                                             help_text='Ключ видео после "v=" (Например https://www.youtube.com/watch?v=JGwWNGJdvx8&index=2&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbAVMG2fOum_KWQU здесь ключем будет "JGwWNGJdvx8" )')
    pdf_file = models.FileField(verbose_name='PDF файл', blank=True)
    word_file = models.FileField(verbose_name='Word файл', blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Lesson, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class ImageSlide(models.Model):
    name = models.CharField(verbose_name='Имя слайдера', max_length=255, blank=True)
    lesson = models.ForeignKey(Lesson, related_name='slider', null=True)
    image = models.ImageField(verbose_name='Картинка слайдера', upload_to=transform('image_slide/'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'


class Part(models.Model):
    title = models.CharField(max_length=255, verbose_name='Раздел')
    image = models.ImageField(upload_to='images/parts', verbose_name='Image')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Test(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='test', null=True, verbose_name='Урок')
    part = models.ForeignKey(Part, related_name='part', null=True, verbose_name='Раздел')

    def __str__(self):
        return str(self.lesson)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestQuestion(models.Model):
    test = models.ForeignKey(Test, verbose_name='Относится к тесту', related_name='test_question')
    type = models.CharField(verbose_name='Тип вопроса', max_length=255, choices=TEST_TYPE_CHOICE, null=True)
    name = models.CharField(verbose_name='Вопрос', max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name='Картинка вопроса', blank=True, null=True,
                              upload_to=transform('question_image/'))
    video = models.CharField(verbose_name='Видео вопроса', max_length=255, blank=True)
    first_association = models.CharField(verbose_name='Первый вариант ответа',
                                         help_text='Это поле заполняется только в случае если вариантом вопроса вы выбрали "Сопоставление", оно будет отображаться как один из возможных ответов',
                                         null=True, blank=True, max_length=255)
    second_association = models.CharField(verbose_name='Второй вариант ответа',
                                          help_text='Это поле заполняется только в случае если вариантом вопроса вы выбрали "Сопоставление", оно будет отображаться как один из возможных ответов',
                                          null=True, blank=True, max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Вопрос к тесту'
        verbose_name_plural = 'Вопросы к тестам'


class TestAnswer(models.Model):
    question = models.ForeignKey(TestQuestion, related_name='test_answer', null=True)
    answer = models.CharField(verbose_name='Ответ', max_length=255, blank=True, null=True)
    true_choice = models.CharField(verbose_name='Относится к варианту',
                                   choices=(('1', 'Первый вариант ответа'), ('2', 'Второй вариант ответа')),
                                   help_text='Здесь вы выбираете вариант ответа который укзали ранее, только если вы выбрали типом вопросв "Сопоставление"',
                                   null=True, blank=True, max_length=255)
    is_correct = models.BooleanField(verbose_name='Правильный ответ', default=False)

    def __str__(self):
        return str(self.answer)

    class Meta:
        verbose_name = 'Ответ к вопросу'
        verbose_name_plural = 'Ответы к вопросам'


class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='exercise_lesson', verbose_name='Урок')

    def __str__(self):
        return str(self.lesson)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'


class ExerciseQuestion(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name='Упражнение', related_name='exercise_question')
    type = models.CharField(verbose_name='Тип вопроса', max_length=255, choices=TEST_TYPE_CHOICE,
                            null=True, default='default')
    name = models.CharField(verbose_name='Вопрос', max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name='Картинка вопроса', blank=True, null=True,
                              upload_to=transform('question_image/'))
    video = models.CharField(verbose_name='Видео вопроса', max_length=255, blank=True)
    first_association = models.CharField(verbose_name='Первый вариант ответа',
                                         help_text='Это поле заполняется только в случае если вариантом вопроса вы выбрали "Сопоставление", оно будет отображаться как один из возможных ответов',
                                         null=True, blank=True, max_length=255)
    second_association = models.CharField(verbose_name='Второй вариант ответа',
                                          help_text='Это поле заполняется только в случае если вариантом вопроса вы выбрали "Сопоставление", оно будет отображаться как один из возможных ответов',
                                          null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            create_thumbnail_image(self.image, self.image, (523, 330))
        super(ExerciseQuestion, self).save()

    class Meta:
        verbose_name = 'Вопрос к упражнению'
        verbose_name_plural = 'Вопросы к упражнению'


class ExerciseAnswer(models.Model):
    question = models.ForeignKey(ExerciseQuestion, verbose_name='Ответ к', related_name='exercise_answer')
    answer = models.CharField(verbose_name='Ответ', max_length=255, blank=True, null=True)
    answer_description = models.TextField(verbose_name='Пояснение ответа', max_length=500,
                                          help_text='Заполняйте это поле, только если ометили галочку правильный ответ',
                                          null=True, blank=True)
    true_choice = models.CharField(verbose_name='Относится к варианту',
                                   choices=(('1', 'Первый вариант ответа'), ('2', 'Второй вариант ответа')),
                                   help_text='Здесь вы выбираете вариант ответа который укзали ранее, только если вы выбрали типом вопросв "Сопоставление"',
                                   null=True, blank=True, max_length=255)
    is_correct = models.BooleanField(verbose_name='Правильный ответ', default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответы к упражнениям'
        verbose_name_plural = 'Ответы к упражнениям'


class Book(models.Model):
    language = models.ForeignKey("Languages", verbose_name='Язык книги', null=True)
    name = models.CharField(verbose_name='Название книжки или методички', max_length=255)
    preview = models.ImageField(verbose_name='Обложка книги или статьи', null=True,
                                upload_to=transform('book_preview/'))
    description = models.TextField(verbose_name='Краткое описание книги', max_length=400, null=True)
    book_file = models.FileField(verbose_name='Файл', upload_to=transform('book_file/'), blank=True, null=True)
    link = models.URLField(verbose_name='Ссылка на ресурс',
                           help_text='Заполнять лишь в том случае, когда вы не загрузили файл', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.preview:
            create_thumbnail_image(self.preview, self.preview, (500, 500))
        super(Book, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Библиотека'


class Projects(models.Model):
    title = models.CharField(verbose_name='Название работы', max_length=255)
    preview = models.ImageField(verbose_name='Превью работы', upload_to=transform('project_preview/'))
    text = RichTextUploadingField(verbose_name='Содрержание работы')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '-' + str(self.pk))
        if self.preview and not self.pk:
            create_thumbnail_image(self.preview, self.preview, (173, 230))
        super(Projects, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Медиапроекты'
        verbose_name = 'Медиапроект'


class InterestingFacts(models.Model):
    image = models.ImageField(verbose_name='Картинка', upload_to=transform('interesting_facts/'))
    lesson = models.ForeignKey(Lesson, verbose_name='Относится к уроку', related_name='facts')

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        if not self.id:
            super(InterestingFacts, self).save(*args, **kwargs)
            resized_image = get_thumbnail(self.image, "1056x750")
            self.image.save(resized_image.name, ContentFile(resized_image.read()), True)
        super(InterestingFacts, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Это интересно'
        verbose_name_plural = 'Это интересно'


class MediaProjectsSlider(models.Model):
    image = models.ImageField(verbose_name='Картинка для слайдера', upload_to=transform('media_projects_slider/'))
    text = models.CharField(verbose_name='Текст на картике', max_length=255)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер на странице медиапроектов'


class Languages(models.Model):
    language = models.CharField(verbose_name='Язык', null=True, max_length=255)

    def __str__(self):
        return self.language


class Results(models.Model):
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    test = models.ForeignKey(Test, verbose_name='Урок')
    user = models.ForeignKey(Users, verbose_name='Пользователь', related_name='results')
    point = models.PositiveIntegerField(verbose_name='Проценты', null=True)
    date = models.DateField(verbose_name='Дата', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.test)


class AboutUs(models.Model):
    class Meta:
        verbose_name = 'Информация о нас'
        verbose_name_plural = 'Информация о нас'

    text = RichTextUploadingField(verbose_name='Текст')

    def __str__(self):
        return "Информация онас"


class Partners(models.Model):
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    title = models.CharField(verbose_name='Название', max_length=255)
    img = models.ImageField(verbose_name='Картинка')
    link = models.URLField(verbose_name='Ссылка')

    def __str__(self):
        return self.title
