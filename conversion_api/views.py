import decimal

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConversionResponse
from .serializers import ConversionResponseSerializer

supported_currencies = ['usd', 'gbp', 'eur']

conversion_rates = {
    "usd_gbp": 0.75,
    "gbp_usd": 1.33,
    "eur_usd": 1.20,
    "usd_eur": 0.83,
    "eur_gbp": 0.90,
    "gbp_eur": 1.11,
}

conversion_rates1 = {
    "usd": {
        "gbp": 0.75,
        "eur": 1.20,
    },
    "gbp": {
        "usd": 1.33,
        "eur": 1.11,
    },
    "eur": {
        "usd": 0.83,
        "gbp": 0.90,
    },
}


class Conversion(APIView):

    def get(self, *args, **kwargs):

        message = 'Conversion success!'
        is_success = True

        currency1 = self.kwargs.get('currency1')
        currency2 = self.kwargs.get('currency2')

        if currency1 not in supported_currencies:
            message = 'currency: ' + currency1 + ' not supported!'
            is_success = False
        if currency2 not in supported_currencies:
            message = 'currency: ' + currency2 + ' not supported!'
            is_success = False

        amount_of_currency1 = float(self.kwargs.get('amount_of_currency1'))

        amount_of_currency2 = decimal.Decimal(0.00)

        if is_success:
            amount_of_currency2 = amount_of_currency1 * conversion_rates1[currency1][currency2]

        response = ConversionResponseSerializer(ConversionResponse(amount_of_currency2, message, is_success))

        return Response(response.data)
