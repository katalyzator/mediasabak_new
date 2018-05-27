from django import forms

from web_app_models.models import Users, Languages
from web_app_models.models import Book


class BooksUploadForm(forms.ModelForm):
    book_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.doc, .docx, .pdf, .djvu,'}), required=False,label='Файл книги')

    class Meta:
        model = Book
        fields = '__all__'


class BooksFilterForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Languages.objects.filter(book__isnull=False).distinct(),
                                      empty_label='Все языки')

    class Meta:
        model = Languages
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'gender', 'email')
