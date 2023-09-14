from typing import Any, Dict
from django import forms

from apps.db_model.models import LinkModel, QRCodeModel

# from apps.utils import requester


class HomeCreateLinkForm(forms.ModelForm):
    force = forms.NullBooleanField()

    class Meta:
        model = LinkModel
        fields = ("long_link", "user", "title")
        widgets = {
            "long_link": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Вставьте ссылку..",
                    "aria-describedby": "inputGroup-sizing-lg",
                }
            )
        }


class QRGeneratorForm(forms.ModelForm):
    class Meta:
        model = QRCodeModel
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control", "style": "height: 180px"}
            )
        }
