from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Comment
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            'text',
            'name',
        }


class ContactForm(forms.Form):
    name = forms.CharField(label='')
    email = forms.EmailField(label='')
    text = forms.CharField(label='', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        text = self.cleaned_data['text']

        messages = EmailMessage(subject=name + 'からの問い合わせ',
                                body=text,
                                from_email=email,
                                to=["kinnkann1991@gmail.com"],
                                cc=[email])

        messages.send()


class SearchForm(forms.Form):
    freeword = forms.CharField(min_length=1, max_length=30, label='', required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        

from django import forms
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email',)
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user