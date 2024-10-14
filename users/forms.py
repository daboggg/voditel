import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль'
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(label="Дата рождения",widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5)),
                                                                                     attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email',
                  'first_name', 'last_name',
                  'date_birth', 'photo',
                  'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'date_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_birth': 'Дата рождения',
            'photo': 'Фотография',
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой e-mail уже существует")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(disabled=True, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(label="Дата рождения",widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5)),
                                                                                     attrs={'class': 'form-control'}))

    class Meta:
        model= get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'date_birth']
        labels = {
            'photo': 'Фото',
        }
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }













