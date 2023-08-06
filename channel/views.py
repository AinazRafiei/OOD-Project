from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from userauth.models import User
from userauth.utils import get_user
from .forms import ChannelForm, PostForm
from .models import Post, Membership, Channel, Share, Tariff


def create_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel_name = form.data['name']
            user = get_user(request)
            ch1 = Channel.objects.create(name=channel_name, owner=user)
            Channel.save(ch1)
            return redirect(reverse_lazy('channels'))
    else:
        form = ChannelForm()
    return render(request, 'html/create_channel.html', {'form': form})


def show_members(request, channel_id):
    if request.method == 'GET':
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            return HttpResponse(status=404)
        members = list(Membership.objects.filter(channel_id=channel_id).values())
        usernames = [User.objects.get(id=i['user_id']).username for i in members]
        user = get_user(request)
        return render(request, 'html/members.html',
                      {'usernames': usernames, 'channel_name': channel.name, "username": user.username})
    return HttpResponse(status=400)


def create_post(request, channel_id):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            price = form.data['price']
            title = form.data['title']
            summary = form.data['summary']
            content = form.data['content']
            channel = Channel.objects.get(id=channel_id)
            user = get_user(request)
            # membership = Membership.objects.get(user=user, channel=channel)
            if channel.owner == user:
                if 'is_vip' in form.data:
                    is_vip = True
                    p1 = Post.objects.create(title=title, price=price, summary=summary, content=content, is_vip=is_vip,
                                             channel=channel, user=user)
                else:
                    is_vip = False
                    p1 = Post.objects.create(title=title, content=content, is_vip=is_vip,
                                             channel=channel, user=user)

                Post.save(p1)
                return redirect(reverse_lazy('channels'))
            else:
                return HttpResponse("you don't have permission")
    else:
        form = PostForm()
    return render(request, 'html/create_post.html', {'form': form})


def represent_post(post, role):
    if role in [Membership.Role.Owner.value, Membership.Role.Admin.value, Membership.Role.Vip.value]:
        return post.represent_full()
    else:
        return post.represent_summary()


def get_role(channel, user):
    if channel.owner_id == user.id:
        return Membership.Role.Owner.value
    try:
        member = Membership.objects.get(user_id=user.id, channel_id=channel.id)
    except Membership.DoesNotExist:
        return ''
    return member.role


class ChannelJoinView(APIView):
    def post(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        channel.members.add(user)
        return Response()


class ChannelLeaveView(APIView):
    def post(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        channel.members.remove(user)
        return Response()


class ChannelDetailView(APIView):
    def get(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        posts = Post.objects.filter(channel_id=channel_id).order_by('published_at')
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        role = get_role(channel, user)
        return Response(
            data=dict(role=role, posts=[represent_post(post, role) for post in posts]))


class ChannelAdminsView(APIView):
    def get(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        if user != channel.owner:
            raise PermissionDenied
        admins = list()
        members = list()
        for member in Membership.objects.filter(channel_id=channel.id):
            if member.role == Membership.Role.Admin.value:
                try:
                    share = Share.objects.get(owner_id=member.user_id, channel_id=channel.id).amount
                except Share.DoesNotExist:
                    share = 0
                admins.append((member.user_id, member.user.username, share))
            else:
                members.append((member.user_id, member.user.username))
        try:
            share = Share.objects.get(owner_id=user.id, channel_id=channel.id).amount
        except Share.DoesNotExist:
            share = 0
        return render(request, 'html/admins.html',
                      {"admins": admins, "members": members, "channel_name": channel.name, "username": user.username,
                       "userid": user.id, "usershare": share})

    def post(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        if user != channel.owner:
            raise PermissionDenied
        userids = dict(request.POST).get('userid')
        for admin in Membership.objects.filter(role=Membership.Role.Admin):
            if admin.user_id not in userids:
                admin.role = Membership.Role.Normal
                admin.save()
        for member in Membership.objects.filter(user_id__in=userids):
            if member.role != Membership.Role.Admin.value:
                member.role = Membership.Role.Admin
                member.save()
        Share.objects.filter(channel_id=channel.id).delete()
        for userid in userids:
            Share.objects.create(channel_id=channel.id, owner_id=userid, amount=request.POST.get(userid))
        return self.get(request, channel_id, *args, **kwargs)


class ChannelTariffsView(APIView):
    def get(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        if user != channel.owner:
            raise PermissionDenied
        tariffs = list()
        for tariff in Tariff.objects.filter(channel_id=channel.id):
            tariffs.append((tariff.get_duration_display(), tariff.duration, tariff.price))
        choices = Tariff.DurationChoice.choices
        return render(request, 'html/tariff.html',
                      {"tariffs": tariffs, "choices": choices, "channel_name": channel.name, "username": user.username})

    def post(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        if user != channel.owner:
            raise PermissionDenied
        durations = dict(request.POST).get('duration')
        Tariff.objects.filter(channel_id=channel.id).delete()
        for duration in durations:
            Tariff.objects.create(channel_id=channel.id, duration=duration, price=request.POST.get(duration))
        return self.get(request, channel_id, *args, **kwargs)


class AllChannelsView(View):
    def get_channel_data(self, channel):
        post = Post.objects.filter(channel_id=channel.id).order_by('-published_at').first()
        summary = ''
        published_at = None
        if post:
            summary = post.represent_summary()[1][:16]
            published_at = post.published_at
        return channel.id, channel.name, summary, published_at.date() if published_at else ''

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if user is None:
            return redirect(reverse_lazy('login'))
        channels = list()
        user_channels = Channel.objects.filter(owner=user)
        user_followings = Channel.objects.filter(id__in=Membership.objects.filter(user=user).values_list("channel_id"))

        def compare_datatime(x, y):
            if y[3] is None:
                return True
            if x[3] is None:
                return False
            return x[3] > y[3]

        # channels.extend(sorted([self.get_channel_data(channel) for channel in user_channels], key=lambda x: x[3]))
        # channels.extend(sorted([self.get_channel_data(channel) for channel in user_followings], key=lambda x: x[3]))
        # channels = sorted(
        #     filter(lambda x: x[3] is not None, [self.get_channel_data(channel) for channel in Channel.objects.all()]),
        #     key=lambda x: x[3])
        channels = [self.get_channel_data(channel) for channel in Channel.objects.all()]
        print(len(channels))
        return render(request, 'html/home.html', {"channels": channels, "username": user.username})
