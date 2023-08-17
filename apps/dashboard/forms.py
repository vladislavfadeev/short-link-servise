from django import forms
from django.contrib.auth.hashers import make_password
from apps.db_model.models import GroupLinkModel, LinkModel, QRCodeModel
from apps.utils import requester


class DashboardLinkForm(forms.ModelForm):
    class Meta:
        model = LinkModel
        fields = ('long_link', 'group', 'slug', 'password', 'date_expire', 'title', 'disabled')
        widgets = {
            'long_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вставьте ссылку..'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Псевдоним'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Задать пароль'}),
            'date_expire': forms.SelectDateWidget(attrs={'class': 'form-select'}, empty_label=("Год", "Месяц", "День")),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'disabled': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if 'password' in self.changed_data:
            pwd = cleaned_data.get('password')
            if pwd is not None:
                cleaned_data['password'] = make_password(pwd)
        url = cleaned_data.get('long_link')
        title = cleaned_data.get('title')
        if url is not None and not title:
            success, title = requester(url)
            if success:
                cleaned_data['title'] = title
            else:
                self.add_error('long_link', title)
        return cleaned_data


class DashboardGroupForm(forms.ModelForm):
    class Meta:
        model = GroupLinkModel
        fields = ('title', 'slug', 'description', 'password', 'date_expire', 'rotation', 'disabled')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название обязательно'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание группы', 'style': 'height: 100px'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Псевдоним'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Задать пароль'}),
            'date_expire': forms.SelectDateWidget(attrs={'class': 'form-select'}, empty_label=("Год", "Месяц", "День")),
            'rotation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disabled': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if 'password' in self.changed_data:
            pwd = cleaned_data.get('password')
            if pwd is not None:
                cleaned_data['password'] = make_password(pwd)
        return cleaned_data
    

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCodeModel
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 180px'})
        }