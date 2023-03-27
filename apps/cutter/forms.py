from django import forms
from .models import LinkModel
from django.core.validators import URLValidator

# class LinkModelForm(forms.Form):
#     long_link = forms.CharField(max_length=30000, 
#                                 validators= ,
#                                 widget=forms.TextInput,
#                                 attrs={'class': 'form-control', 
#                                       'placeholder': 'Вставьте ссылку..'})

class LinkModelForm(forms.ModelForm):
     class Meta:
        model = LinkModel
        fields = ('long_link', 'statistics')
        widgets = {
            'long_link': forms.TextInput(attrs={'class': 'form-control', 
                                                'placeholder': 'Вставьте ссылку..'},
                                        ),
            'statistics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
          }


    # class Meta:
    #     model = LinkModel
    #     fields = ['long_link']
    #     labels = {
    #         'name': 'Имя',
    #         'last_name': 'Фамилия',
    #         'rating': 'Рейтинг',
    #         'feedback': 'Ваш отзыв',
    #     }