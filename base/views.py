import requests
from conversion_api.models import ConversionResponse
from conversion_api.serializers import ConversionResponseSerializer
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserLoginForm


@login_required(login_url='/login')
def home(request):
    return redirect('account')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:

                login(request, user)

                if user.is_staff:
                    return redirect('admin')
                else:
                    return redirect('account')

            else:
                messages.error(request, 'Username or password incorrect!')
    else:
        form = CustomUserLoginForm()

    return render(request, 'base/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration done! Please login!')

            # check if selected currency is GBP, if not then convert and save that amount
            if not (form.cleaned_data['currency'] == 'gbp'):

                print('convert!')

                user = CustomUser.objects.get(username=form.cleaned_data['username'])

                # make request url and call api, 1000.00 is the default gbp amount
                url = 'gbp' + '/' + form.cleaned_data['currency'] + '/' + '1000.00'
                absolute_uri = request.build_absolute_uri('/conversion/' + url)
                response = requests.get(absolute_uri)

                # deserialize response and create ConversionResponse object
                serializer = ConversionResponseSerializer(data=response.json())
                if serializer.is_valid():
                    conversion_response = ConversionResponse(serializer.validated_data['amount'],
                                                             serializer.validated_data['message'],
                                                             serializer.validated_data['is_success'])

                    # if something went wrong in the conversion then just save it with the default value
                    if conversion_response.is_success:
                        user.account_balance = conversion_response.amount
                        user.save()

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'base/register.html', {'form': form})


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login')
