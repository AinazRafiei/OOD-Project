from django import forms

from .models import Channel, Post


class ChannelForm(forms.Form):
    name = forms.CharField()

    class Meta:
        model = Channel


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['is_vip', 'price', 'title', 'summary', 'content']
        widgets = {
            'is_vip': forms.CheckboxInput,
            'price': forms.NumberInput,
            'title': forms.TextInput,
            'summary': forms.TextInput,
            'content': forms.Textarea,
        }

    field_order = ['title', 'content', 'is_vip', 'summary', 'price']

    def clean(self):
        cleaned_data = super().clean()
        is_vip = cleaned_data.get('is_vip')
        price = cleaned_data.get('price')
        title = cleaned_data.get('title')
        summary = cleaned_data.get('summary')

        if is_vip:
            if not price:
                raise forms.ValidationError("Price field for vip post is required.")
            if not title:
                raise forms.ValidationError("Title field for vip post is required.")
            if not summary:
                raise forms.ValidationError("Summary field for vip post is required.")

        return cleaned_data
