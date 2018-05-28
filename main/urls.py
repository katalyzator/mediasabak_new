"""mediasabak_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from main import settings
from web_app_views.views import *
from web_app_views.views import *

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexTemplateView.as_view(), name='index'),
    url(r'^get_certificate/$', login_required(PDFTemplateView), name='certificate'),
    url(r'^user/(?P<slug>[\w-]+)/$', UserProfileUpdate.as_view(), name='user_profile'),
    url(r'^about/$', AboutTemplateView.as_view(), name='about'),
    url(r'^parts/$', PartListView.as_view(), name='parts'),
    url(r'^all_lessons/$', LessonListView.as_view(), name='all_lessons'),
    url(r'^lesson/(?P<slug>[\w-]+)/$', LessonDetailView.as_view(), name='lesson_detail'),
    url(r'^lessons_for_test/(?P<id>[\w-]+)/$', TestLessonListView.as_view(), name='test'),
    url(r'^test/(?P<slug>[\w-]+)/$', LessonDetailView.as_view(), name='test_detail'),
    url(r'^get_next_question/(?P<question_id>\d+)/(?P<test_id>\d+)$', test_next_question, name='get_next_question'),
    url(r'^check_answers/(?P<question_id>\d+)', check_answer, name='check_answers'),
    url(r'^get_next_exercise_question/(?P<question_id>\d+)/(?P<exercise_id>\d+)$', get_next_exercise_question,
        name='get_next_exercise_question'),
    url(r'^books/$', BooksListView.as_view(), name='books'),
    url(r'^projects/$', MediaProjectsListView.as_view(), name='projects'),
    url(r'^projects/(?P<slug>[\w-]+)/$', MediaProjectsDetailView.as_view(), name='project_detail'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
