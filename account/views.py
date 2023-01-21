from django.contrib.auth.models import auth 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from account.forms import RegistrationForm, ProfileForm
from .models import Profile

# Authentication Building Function import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView
from django.contrib import messages




def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You Are Authenticate!")
    else:
        form = RegistrationForm
        if request.method == 'post' or request.method == 'POST':
            form = RegistrationForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Login Successful')
                return redirect('login')
                # return HttpResponse("Account bas been Created!")

        contex = {
            'form': form
        }

    return render(request, 'accounts/register.html', contex)



def userlogin(request):
    if request.user.is_authenticated:
        return HttpResponse('You are logged in!')
    else:
        if request.method == 'POST' or request.method == 'post':
            username = request.POST.get('username')
            password = request.POST.get('password')
            my_user = authenticate(request, username=username, password=password)
            if my_user is not None:
                login(request, my_user)
                return redirect('/')
            else:
                return HttpResponse('404')

    return render(request, 'accounts/login.html')


# def logout(request):
#     if request.user.is_authenticated:
#         auth.logout(request)
#         return redirect('/login')



class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        profile_obj = Profile.objects.get(user=request.user)
        profileForm = ProfileForm(instance=profile_obj)

        context = {

            'profileForm':profileForm,
        }
        return render(request, 'profile.html', context)


    # def post(self, request, *args, **kwargs):
    #     if request.method == 'post' or request.method == 'POST':
    #         billingaddress = BillingAddress.objects.get(user=request.user)
    #         billingaddress_form = BillingAddressForm(request.POST, instance=billingaddress)
    #         profile_obj = Profile.objects.get(user=request.user)
    #         profileForm = ProfileForm(request.POST, instance=profile_obj)
    #         if billingaddress_form.is_valid() or profileForm.is_valid():
    #             billingaddress_form.save()
    #             profileForm.save()
    #             return redirect('account:profile')
