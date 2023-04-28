from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from transfer.models import Transfer
from request.models import Request
from django.db.models import Q


@login_required(login_url='/login')
def history(request):
    user_email = request.user.email

    outgoing_transfers = Transfer.objects.filter(sender_email=user_email).order_by('-date')
    incoming_transfers = Transfer.objects.filter(receiver_email=user_email).order_by('-date')

    outgoing_requests = Request.objects.filter(
        Q(receiver_email=request.user.email) &
        Q(pending=False)) \
        .order_by('-date_requested')

    incoming_requests = Request.objects.filter(
        Q(patron_email=request.user.email) &
        Q(pending=False)) \
        .order_by('-date_requested')

    context = {
        'outgoing_transfers': outgoing_transfers,
        'incoming_transfers': incoming_transfers,
        'outgoing_requests': outgoing_requests,
        'incoming_requests': incoming_requests,
    }

    return render(request, 'history/history.html', context)
