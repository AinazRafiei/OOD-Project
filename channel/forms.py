from django import forms
from .models import Channel, Post, Media



class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name']


class PostForm(forms.ModelForm):
    media_file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['price', 'title', 'summary', 'content']

    def clean(self):
        cleaned_data = super().clean()
        media = cleaned_data.get('media')
        media_file = self.cleaned_data.get('media_file')
        price = cleaned_data.get('price')

        if media_file and not media:
            raise forms.ValidationError("Please select a media type.")

        if media and not media_file:
            for field in ['size', 'format', 'type', 'duration']:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required when a file is uploaded.")

        if price and price <= 0:
            self.add_error('price', "Price must be a positive integer.")

    def save(self, commit=True):
        media_file = self.cleaned_data.get('media_file')
        if media_file:
            media = Media.objects.create(
                size=self.cleaned_data['size'],
                format=self.cleaned_data['format'],
                type=self.cleaned_data['type'],
                duration=self.cleaned_data['duration']
            )
            self.instance.media = media

        return super().save(commit=commit)
