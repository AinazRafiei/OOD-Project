from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from userauth.utils import get_user
from .forms import WithdrawForm, ChargeForm
from .models import Wallet


class UserBalanceAPIView(APIView):
    def get(self, request):
        user = get_user(request)
        user_wallet = Wallet.objects.get_or_create(user=user)
        return render(request, 'html/show_amount.html',
                      {'balance': "%.2f" % user_wallet[0].balance, 'charge_form': ChargeForm, 'withdraw_form': WithdrawForm})


class ChargeAPIView(APIView):
    form_class = ChargeForm
    success_url = reverse_lazy('wallet')
    template_name = 'html/show_amount.html'

    def post(self, request):
        user = get_user(request)
        form = ChargeForm(request.data)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user.wallet.balance += amount
            user.wallet.save()
            return redirect(reverse_lazy('wallet') + '?message=charge_success')
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawAPIView(APIView):
    def post(self, request):
        user = get_user(request)
        form = WithdrawForm(request.data)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= user.wallet.balance:
                user.wallet.balance -= amount
                user.wallet.save()
                return redirect(reverse_lazy('wallet') + '?message=withdraw_success')
            else:
                return redirect(reverse_lazy('wallet') + '?message=withdraw_faild')
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
