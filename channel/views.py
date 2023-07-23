from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .forms import ChannelForm, PostForm
from .models import Channel, Post, Membership


# Create your views here.


def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel_name = form.data['name']
            user_id = request.user.id
            ch1 = Channel.objects.create(name=channel_name, owner=user_id)
            Channel.save(ch1)
            return redirect('channel_created')
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
            media = form.data['media']
            is_vip = form.data['is_vip']
            channel_id = channel_id
            user_id = request.user.id
            membership = Membership.objects.get(user_id=user_id)
            if membership.role == 'admin':
                p1 = Post.objects.create(title=title, price=price, summary=summary, content=content, media=media, is_vip=is_vip, channel_id=channel_id, user_id=user_id)
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
