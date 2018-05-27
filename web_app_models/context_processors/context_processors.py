from allauth.account.forms import SignupForm, LoginForm
from allauth.account.views import login
from django.http import JsonResponse

from web_app_models.models import Users


def login_form(request):
    login_form = LoginForm(request.POST)
    context = {
        'login_form': login_form
    }
    return context


def signup(request):
    form = SignupForm(request.POST)
    context = {
        'signup_form': form
    }
    return context
