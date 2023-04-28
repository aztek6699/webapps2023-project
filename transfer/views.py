from decimal import Decimal
import requests
from base.models import CustomUser
from conversion_api.models import ConversionResponse
from conversion_api.serializers import ConversionResponseSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import render
from .models import Transfer
from .forms import TransferForm


def get_converted_amount(request, user_cur, rec_curr, amount):
    url = user_cur + '/' + rec_curr + '/' + str(amount)

    absolute_uri = request.build_absolute_uri('/conversion/' + url)
    response = requests.get(absolute_uri)

    # deserialize response and create ConversionResponse object
    serializer = ConversionResponseSerializer(data=response.json())
    if serializer.is_valid():
        conversion_response = ConversionResponse(serializer.validated_data['amount'],
                                                 serializer.validated_data['message'],
                                                 serializer.validated_data['is_success'])

        # check if api call was successful assign new converted amount else do something???
        # TODO: figure out the else part
        if conversion_response.is_success:
            return Decimal(conversion_response.amount)
        else:
            messages.error(request, conversion_response.message)
            return Decimal(-1)


@login_required(login_url='/login')
def create_transfer(request, email=None):
    receiver = CustomUser.objects.get(email=email)
    context = {
        'receiver': receiver,
    }

    if request.method == 'POST':
        form = TransferForm(request.POST)

        context.update({'form': form})

        if form.is_valid():
            amount = Decimal(form.cleaned_data['amount'])
            user = request.user

            # check if user has enough money
            if not user.account_balance > amount:
                messages.error(request, 'Insufficient balance!')
            else:
                converted_amount = Decimal(0.00)
                # if the currency don't match convert
                if not user.currency == receiver.currency:
                    converted_amount = get_converted_amount(request, user.currency, receiver.currency, amount)

                # if less then 0, i.e: -1 then conversion api sent an error so dont do anything
                if converted_amount >= 0:
                    user_prev_bal = user.account_balance
                    user.account_balance -= amount

                    receiver_prev_bal = receiver.account_balance
                    if converted_amount > 0.00:
                        receiver.account_balance += converted_amount
                    else:
                        receiver.account_balance += amount

                    new_transaction = Transfer(
                        sender_email=user.email,
                        receiver_email=receiver.email,
                        amount=amount,
                        converted_amount=converted_amount,
                        sender_prev_amount=user_prev_bal,
                        sender_new_amount=user.account_balance,
                        receiver_prev_amount=receiver_prev_bal,
                        receiver_new_amount=receiver.account_balance,
                        sender_currency_at_time=user.currency,
                        receiver_currency_at_time=receiver.currency,
                    )

                    try:
                        with transaction.atomic():
                            user.save()
                            receiver.save()
                            new_transaction.save()
                            messages.success(request, 'Transfer complete!')
                    except IntegrityError as e:
                        messages.error(request, "Database write error!")
                        print(e)

    else:
        form = TransferForm()
        context.update({'form': form})

    return render(request, 'transfer/create_transfer.html', context)
