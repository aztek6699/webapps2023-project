from base.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, ButtonHolder, Column
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomAdminCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Column(Field('username', placeholder="Username", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('email', placeholder="Email", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('password1', placeholder="Password", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('password2', placeholder="Re-Enter Password", css_class="text-center"),
                   css_class='col-md-4 mx-auto'),
            Column(Field('first_name', placeholder="First Name", css_class="text-center"),
                   css_class='col-md-4 mx-auto'),
            Column(Field('last_name', placeholder="Last Name", css_class="text-center"), css_class='col-md-4 mx-auto'),
            ButtonHolder(
                Submit('submit', 'Register', css_class='btn-primary'),
                css_class="text-center"
            )
        )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]
