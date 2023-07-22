from django import forms

from .models import Channel


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name']


from django import forms
from .models import Post, Media


class PostForm(forms.ModelForm):
    media_file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['is_vip', 'price', 'title', 'summary', 'content', 'media', 'media_file']

    def clean(self):
        cleaned_data = super().clean()
        is_vip = cleaned_data.get('is_vip')
        media_file = cleaned_data.get('media_file')
        price = cleaned_data.get('price')
        title = cleaned_data.get('title')
        summary = cleaned_data.get('summary')
        content = cleaned_data.get('content')
        media = cleaned_data.get('media')

        if is_vip:
            if not all([price, title, summary]):
                raise forms.ValidationError("Title, summary, and price are required for VIP posts.")
        else:
            cleaned_data['price'] = None
            cleaned_data['title'] = None
            cleaned_data['summary'] = None

        if not content:
            raise forms.ValidationError("Content field is required.")

        if media_file and not media:
            raise forms.ValidationError("Please select a media type.")

        return cleaned_data

    def save(self, commit=True):
        media_file = self.cleaned_data.get('media_file')
        media = self.cleaned_data.get('media')

        if media_file and not media:
            media = Media.objects.create(
                size=self.cleaned_data['size'],
                format=self.cleaned_data['format'],
                type=self.cleaned_data['type'],
                duration=self.cleaned_data['duration']
            )
            self.instance.media = media

        return super().save(commit=commit)
