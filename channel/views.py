from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .forms import ChannelForm, PostForm
from .models import Channel, Post, Membership
from userauth.utils import get_user
from django.urls import reverse_lazy
from userauth.models import User



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


def show_members(request, channel_id):
    if request.method == 'GET':
        members = list(Membership.objects.filter(channel_id=channel_id).values())
        usernames = [User.objects.get(id=i['user_id']).username for i in members]
    return render(request, 'html/show_members.html', {'usernames': usernames})


def create_post(request, channel_id):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            price = form.data['price']
            title = form.data['title']
            summary = form.data['summary']
            content = form.data['content']
            if form.data['is_vip'] is 'on':
                is_vip = True
            else:
                is_vip = False
            channel = Channel.objects.get(id=channel_id)
            user = get_user(request)
            # membership = Membership.objects.get(user=user, channel=channel)
            if channel.owner == user:
                p1 = Post.objects.create(title=title, price=price, summary=summary, content=content, is_vip=is_vip, channel=channel, user=user)
                Post.save(p1)
                return redirect(reverse_lazy('home'))
            else:
                return HttpResponse("you don't have permission")
    else:
        form = PostForm()
    return render(request, 'html/create_post.html', {'form': form})


class ChannelPostViews(View):
    def get(self, request, channel_id, *args, **kwargs):
        pass
