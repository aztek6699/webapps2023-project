import requests
from conversion_api.models import ConversionResponse
from conversion_api.serializers import ConversionResponseSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import ChangeCurrencyForm


@login_required(login_url='/login')
def account_page(request):
    if request.method == 'POST':
        form = ChangeCurrencyForm(request.POST)
        if form.is_valid():
            user = request.user

            previous_currency = user.currency
            new_currency = form.cleaned_data['currency']

            # make request url and call api
            url = previous_currency + '/' + new_currency + '/' + str(user.account_balance)
            absolute_uri = request.build_absolute_uri('/conversion/' + url)
            response = requests.get(absolute_uri)

            # deserialize response and create ConversionResponse object
            serializer = ConversionResponseSerializer(data=response.json())
            if serializer.is_valid():
                conversion_response = ConversionResponse(serializer.validated_data['amount'],
                                                         serializer.validated_data['message'],
                                                         serializer.validated_data['is_success'])

                # check if api call was successful: save new amount and new currency to user
                # else show error message
                if conversion_response.is_success:
                    user.account_balance = conversion_response.amount
                    user.currency = form.cleaned_data['currency']
                    user.save()
                    messages.success(request, 'Currency updated!')
                else:
                    messages.error(request, conversion_response.message)

    else:
        current_currency = request.user.currency
        form = ChangeCurrencyForm(initial={'currency': current_currency})

    return render(request, 'account/account.html', {'form': form})
