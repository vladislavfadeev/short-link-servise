from django import forms
from apps.db_model.models import GroupLinkModel, LinkModel
from apps.utils import requester


class DashboardLinkForm(forms.ModelForm):
    class Meta:
        model = LinkModel
        fields = ('long_link', 'group', 'slug', 'password', 'date_expire', 'title', 'is_active')
        widgets = {
            'long_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вставьте ссылку..'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Псевдоним'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Задать пароль'}),
            'date_expire': forms.SelectDateWidget(attrs={'class': 'form-select'}, empty_label=("Год", "Месяц", "День")),
            'group': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Дата'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('force'):
            return cleaned_data
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
        fields = ('title', 'slug', 'description', 'password', 'date_expire', 'rotation', 'is_active')
        widgets = {
            'long_link': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Вставьте ссылку..',
                    'aria-describedby': 'inputGroup-sizing-lg',
                }
            )
        }
