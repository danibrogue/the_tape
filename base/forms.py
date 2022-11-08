from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

from base.models import Article, Subscriber


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class NewUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    username = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_username'}))

    class Meta:
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class NewsletterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name'})
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'})
    )

    class Meta:
        model = Subscriber
        fields = '__all__'
