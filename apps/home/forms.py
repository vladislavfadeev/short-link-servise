from django import forms
from apps.db_model.models import LinkModel


class HomeCreateLinkForm(forms.ModelForm):
    class Meta:
        model = LinkModel
        fields = ('long_link',)
        widgets = {
            'long_link': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Вставьте ссылку..',
                    'aria-describedby': 'inputGroup-sizing-lg',
                }
            )
        }
