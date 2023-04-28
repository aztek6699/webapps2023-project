from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from .forms import CustomAdminCreationForm
from django.contrib import messages
from base.models import CustomUser
from transfer.models import Transfer
from request.models import Request


@staff_member_required
def home(request):
    return redirect('all_user')


@staff_member_required
def all_user(request):
    queryset = CustomUser.objects.all()
    return render(request, 'admin/user.html', {"users": queryset})


@staff_member_required
def all_transfer(request):
    queryset = Transfer.objects.all().order_by('date')
    return render(request, 'admin/transfer.html', {"transfers": queryset})


@staff_member_required
def all_request(request):
    queryset = Request.objects.all().order_by('date_requested')
    return render(request, 'admin/request.html', {"requests": queryset})


@staff_member_required
def register_new_admin(request):
    if request.method == 'POST':
        form = CustomAdminCreationForm(request.POST)
        if form.is_valid():

            try:
                with transaction.atomic():
                    new_admin = form.save()
                    new_admin.is_staff = True
                    new_admin.is_superuser = True
                    new_admin.is_active = True
                    new_admin.save()
            except IntegrityError as e:
                messages.error(request, "Database write error!")
                print(e)

            messages.success(request, 'New admin created!')
    else:
        form = CustomAdminCreationForm()

    return render(request, 'admin/register.html', {'form': form})
