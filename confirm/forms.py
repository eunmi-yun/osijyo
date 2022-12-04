from django import forms
from confirm.models import image

class ImageForm(forms.ModelForm):
    class Meta:
        model = image
        fields = ['image',]
        label ={
            'image':'이미지 파일',
        }