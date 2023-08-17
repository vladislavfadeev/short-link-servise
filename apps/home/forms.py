from typing import Any, Dict
from django import forms

from apps.db_model.models import LinkModel, QRCodeModel
from apps.utils import requester


class HomeCreateLinkForm(forms.ModelForm):
    class Meta:
        model = LinkModel
        fields = ('long_link', 'user', 'title')
        widgets = {
            'long_link': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Вставьте ссылку..',
                    'aria-describedby': 'inputGroup-sizing-lg',
                }
            )
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if cleaned_data.get('force'):
            return cleaned_data
        url = cleaned_data.get('long_link')
        success, title = requester(url)
        if success:
            cleaned_data['title'] = title
        else:
            self.add_error('long_link', title)
        return cleaned_data


class QRGeneratorForm(forms.ModelForm):
    class Meta:
        model = QRCodeModel
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 180px'})
        }