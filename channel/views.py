import datetime

from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from userauth.models import User
from userauth.utils import get_user, Authentication, login_required
from .forms import ChannelForm, PostForm, TariffFrom
from .models import Post, Membership, Channel, Share, Tariff, Subscription, PurchasedPost
from .utils import buy


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
        return render(request, 'html/members.html',
                      {'usernames': usernames, 'channel_name': channel.name})
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
                    Post.objects.create(title=title, price=price, summary=summary, content=content, is_vip=is_vip,
                                        channel=channel, user=user)
                else:
                    is_vip = False
                    Post.objects.create(title=title, content=content, is_vip=is_vip,
                                        channel=channel, user=user)

                return redirect(reverse_lazy('channels'))
            else:
                return HttpResponse("you don't have permission")
    else:
        form = PostForm()
    return render(request, 'html/create_post.html', {'form': form})


def represent_post(post, role, purchased_posts):
    if role in [Membership.Role.Owner.value, Membership.Role.Admin.value, Membership.Role.Vip.value]:
        return post.represent_full()
    elif post.id in purchased_posts:
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


class SubscribeView(FormView):
    form_class = TariffFrom
    template_name = 'html/subscribe.html'

    def post(self, request, channel_id, *args, **kwargs):
        form = self.get_form()
        user = get_user(request)
        tariff = Tariff.objects.get(id=form.data['tariff'])
        membership = Membership.objects.get(channel_id=channel_id, user=user)
        if user.wallet.balance < tariff.price:
            return ValidationError
        buy(user, channel_id, tariff.price)
        Subscription.objects.create(user=membership,
                                    until_date=datetime.datetime.now() + datetime.timedelta(
                                        days=tariff.duration))
        membership.role = Membership.Role.Vip
        membership.save()
        return redirect(reverse_lazy('channels'))


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
        Share.objects.filter(owner=user, channel=channel).delete()
        return Response()


class ChannelDetailView(APIView):
    def get(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        purchased_posts = list(PurchasedPost.objects.filter(user=user).values_list('post_id', flat=True))
        posts = Post.objects.filter(channel_id=channel_id).order_by('published_at')
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            raise NotFound
        role = get_role(channel, user)
        return Response(
            data=dict(role=role, posts=[represent_post(post, role, purchased_posts) for post in posts]))


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
                      {"tariffs": tariffs, "choices": choices, "channel_name": channel.name})

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

    @login_required
    def get(self, request, *args, **kwargs):
        user = get_user(request)
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
        return render(request, 'html/home.html', {"channels": channels})


class PurchasePostView(APIView):
    def get(self, request, channel_id, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return NotFound
        return render(request, 'html/purchase_post.html',
                      {'channel_id': channel_id, 'title': post.title, 'summary': post.summary, 'price': post.price,
                       'time': post.published_at, 'channel_name': post.channel.name})

    def post(self, request, channel_id, post_id, *args, **kwargs):
        user = get_user(request)
        if not user:
            return redirect(reverse_lazy('login'))
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return NotFound
        if PurchasedPost.objects.filter(post=post, user=user).exists():
            return redirect(reverse_lazy('channels'))
        if user.wallet.balance < post.price:
            return ValidationError
        buy(user, channel_id, post.price)
        PurchasedPost.objects.create(post=post, user=user)
        return redirect(reverse_lazy('channels'))
