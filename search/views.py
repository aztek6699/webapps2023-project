from base.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .forms import SearchForm


@login_required(login_url='/login')
def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if 'search' in request.GET:

            if not form.data['email'] and not form.data['name']:
                messages.error(request, 'Enter user email or name!')
            else:
                if form.is_valid():

                    result = None

                    # only search name case as email is empty
                    if not form.data['email']:
                        result = CustomUser.objects.filter(Q(first_name__icontains=form.cleaned_data['name']) |
                                                           Q(last_name__icontains=form.cleaned_data['name'])) \
                            .exclude(email=request.user.email)
                    # only search email case as name is empty
                    elif not form.data['name']:
                        result = CustomUser.objects.filter(email__icontains=form.cleaned_data['email']) \
                            .exclude(email=request.user.email)
                    # both email and name provided
                    else:
                        result = CustomUser.objects.filter(Q(first_name__icontains=form.cleaned_data['name']) |
                                                           Q(last_name__icontains=form.cleaned_data['name']) |
                                                           Q(email__icontains=form.cleaned_data['email'])
                                                           ).exclude(email=request.user.email)

                    if not result:
                        messages.error(request, 'No users found!')
                    else:
                        return search_result(request, result)

    else:
        form = SearchForm()

    return render(request, 'search/search.html', {'form': form})


def search_result(request, queryset=None):
    return render(request, 'search/result.html', {"results": queryset})
