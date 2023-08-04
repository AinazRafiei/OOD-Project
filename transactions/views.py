from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Wallet
from .forms import WithdrawForm, ChargeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from userauth.utils import get_user
from django.core.exceptions import ValidationError



class UserBalanceAPIView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_wallet = Wallet.objects.get_or_create(user=user)
        return render(request, 'html/show_amount.html',
                      {'username': user.username, 'balance': user_wallet[0].balance, 'charge_form': ChargeForm,
                       'withdraw_form': WithdrawForm})


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
            return redirect(reverse_lazy('wallet', args=[user.id]) + '?message=charge_success')
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
                return redirect(reverse_lazy('wallet', args=[user.id]) + '?message=withdraw_success')
            else:
                return redirect(reverse_lazy('wallet', args=[user.id]) + '?message=withdraw_faild')
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)