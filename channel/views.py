from django.shortcuts import render, redirect
from .forms import ChannelForm, PostForm


# Create your views here.


def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('channel_created')
    else:
        form = ChannelForm()
    return render(request, 'html/create_channel.html', {'form': form})



def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_created')
    else:
        form = PostForm()
    return render(request, 'html/create_post.html', {'form': form})

