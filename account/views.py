from django.contrib.auth.models import auth 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from account.forms import RegistrationForm, ProfileForm
from .models import Profile, MyUser

# Authentication Building Function import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView
from django.contrib import messages

def register(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			# login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('account:login')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'accounts/register.html', context)


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    else:
        if request.method == 'POST' or request.method == 'post':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try: 
                my_user = authenticate(request, username=username, password=password)
            except:
                messages.warning(request, 'User does not exits!')

            if my_user is not None:
                login(request, my_user)
                return redirect('dashboard:dashboard')
            else:
                messages.warning(request, 'User does not exits!')

    return render(request, 'accounts/login.html')


# def logout(request):
#     if request.user.is_authenticated:
#         auth.logout(request)
#         return redirect('/login')



class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        profile_obj = Profile.objects.get(user=request.user)
        queary_set = MyUser.objects.all()
        profileForm = ProfileForm(instance=profile_obj)
        context = {
            'queary_set': queary_set,
            'profile_obj': profile_obj,
            'profileForm': profileForm,
        }
        return render(request, 'profile.html', context)


