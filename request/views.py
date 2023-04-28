from datetime import datetime
from decimal import Decimal

import requests
from base.models import CustomUser
from conversion_api.models import ConversionResponse
from conversion_api.serializers import ConversionResponseSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from .forms import RequestForm
from .models import Request


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

        # check if api call was successful assign new converted amount else show error message
        if conversion_response.is_success:
            return Decimal(conversion_response.amount)
        else:
            messages.error(request, conversion_response.message)
            return Decimal(-1)


@login_required(login_url='/login')
def create_request(request, email=None):
    patron = CustomUser.objects.get(email=email)
    context = {
        'patron': patron,
    }

    if request.method == 'POST':
        form = RequestForm(request.POST)

        context.update({'form': form})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user

            converted_amount = Decimal(0.00)
            if not user.currency == patron.currency:
                converted_amount = get_converted_amount(request, user.currency, patron.currency, amount)

            if converted_amount >= 0:
                new_request = Request(
                    patron_email=patron.email,
                    receiver_email=user.email,
                    amount=amount,
                    converted_amount=converted_amount,
                    patron_currency_at_time=patron.currency,
                    receiver_currency_at_time=user.currency,
                    accepted=False,
                    pending=True,
                )

                try:
                    with transaction.atomic():
                        new_request.save()
                        messages.success(request, "Request Creation Successful!")
                except IntegrityError as e:
                    messages.error(request, "Database write error!")
                    print(e)

    else:
        form = RequestForm()
        context.update({'form': form})

    return render(request, 'request/create_request.html', context)


@login_required(login_url='/login')
def pending_request(request):
    outgoing_requests = Request.objects.filter(
        Q(receiver_email=request.user.email) &
        Q(pending=True)) \
        .order_by('-date_requested')

    incoming_requests = Request.objects.filter(
        Q(patron_email=request.user.email) &
        Q(pending=True)) \
        .order_by('-date_requested')

    context = {
        'outgoing_requests': outgoing_requests,
        'incoming_requests': incoming_requests,
    }

    return render(request, 'request/pending_requests.html', context)


@login_required(login_url='/login')
def accept_request(request, req_id):

    req_obj = Request.objects.get(pk=req_id)

    if req_obj is not None:
        patron = request.user

        amount = req_obj.amount

        if req_obj.converted_amount > 0:
            amount = req_obj.converted_amount

        if patron.account_balance > amount:

            try:
                receiver = CustomUser.objects.get(email=req_obj.receiver_email)

                with transaction.atomic():

                    req_obj.patron_prev_amount = patron.account_balance
                    req_obj.receiver_prev_amount = receiver.account_balance

                    patron.account_balance -= amount
                    receiver.account_balance += amount

                    req_obj.patron_new_amount = patron.account_balance
                    req_obj.receiver_new_amount = receiver.account_balance

                    req_obj.accepted = True
                    req_obj.pending = False
                    req_obj.date_completed = datetime.now()

                    patron.save()
                    receiver.save()
                    req_obj.save()

                    messages.success(request, 'Request Completion Successful!')

            except IntegrityError as e:
                messages.error(request, 'Database write error!')
                print(e)

            except Exception as e:
                messages.error(request, 'Something went wrong!')
                print(e)

        else:
            messages.error(request, 'Insufficient Balance!')

    return HttpResponse()


@login_required(login_url='/login')
def reject_request(request, req_id):

    req_obj = Request.objects.get(pk=req_id)

    if req_obj is not None:

        patron = request.user
        receiver = CustomUser.objects.get(email=req_obj.receiver_email)

        req_obj.patron_new_amount = patron.account_balance
        req_obj.patron_prev_amount = patron.account_balance
        req_obj.receiver_new_amount = receiver.account_balance
        req_obj.receiver_prev_amount = receiver.account_balance

        req_obj.pending = False
        req_obj.accepted = False

        req_obj.date_completed = datetime.now()

        try:
            with transaction.atomic():
                req_obj.save()
                messages.success(request, "Request Rejection Successful!")
        except IntegrityError as e:
            messages.error(request, "Database write error!")
            print(e)
        except Exception as e:
            messages.error(request, "Something went wrong!")
            print(e)

    return HttpResponse()


@login_required(login_url='/login')
@transaction.atomic
def cancel_request(request, req_id):
    Request.objects.get(pk=req_id).delete()
    messages.success(request, "Request Cancellation Successful!")
    return HttpResponse()
