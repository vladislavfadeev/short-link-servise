from authuser.forms import CustomUserCreationForm, CustomAuthenticationForm
from authuser.utils import send_email_verify, get_redirect_url
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views import View
from django.contrib.auth import views


User = get_user_model()


class CustomLoginView(views.LoginView):
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm


class CreateUserView(View):
    template_name = 'authuser/registration/register.html'

    def get(self, request):

        if get_redirect_url() and self.request.user.is_authenticated:
            redirect_to = get_redirect_url()
            return redirect(redirect_to)
        
        context = {
            'form': CustomUserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email,
                                password=password)
            send_email_verify(request, user)
            return redirect('email_confirm')
            # login(request, user)
            # return redirect('home')
        
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    


class EmailVerifyView(View):
    
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return redirect('email_verify_invalid')


    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
