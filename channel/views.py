from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .forms import ChannelForm, PostForm
from .models import Channel, Post, Membership
from userauth.utils import get_user, get_user_id
from django.urls import reverse_lazy



# Create your views here.


def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel_name = form.data['name']
            user = get_user(request)
            ch1 = Channel.objects.create(name=channel_name, owner=user)
            Channel.save(ch1)
            return redirect(reverse_lazy('home'))
    else:
        form = ChannelForm()
    return render(request, 'html/create_channel.html', {'form': form})


def create_post(request, channel_id):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            price = form.data['price']
            title = form.data['title']
            summary = form.data['summary']
            content = form.data['content']
            is_vip = form.data['is_vip']
            channel = Channel.objects.get(id=channel_id)
            user = get_user(request)
            membership = Membership.objects.get(user=user, channel=channel)
            if membership.role == 'admin':
                p1 = Post.objects.create(title=title, price=price, summary=summary, content=content, is_vip=is_vip, channel=channel, user=user)
                Post.save(p1)
                return redirect('post_created')
            else:
                return HttpResponse("you don't have permission")
    else:
        form = PostForm()
    return render(request, 'html/create_post.html', {'form': form})


class ChannelPostViews(View):
    def get(self, request, channel_id, *args, **kwargs):
        pass
