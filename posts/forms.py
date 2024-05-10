from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'placeholder': 'Заголовок', 'class': 'input input-bordered w-full max-w-xs'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-input form-input_desc'}))
    cost = forms.IntegerField(required=False, min_value=None, label='Цена (в тенге)', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    image = forms.ImageField(label='Фото', widget=forms.FileInput(attrs={'class': 'form-image form-control'}), required=False)
    class Meta:
        model = Post
        fields = ('title', 'description', 'cost', 'image')


class PostDeleteForm(forms.Form):
    is_sells = forms.BooleanField(label='Вы точно уверенны?', required=False)
