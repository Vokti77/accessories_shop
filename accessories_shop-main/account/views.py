from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from account.models import MyUser

from account.forms import ProfileForm, RegistrationForm


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileForm(instance=self.request.user.profile)
        return context


@login_required(login_url="account:login")
def profile_update(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("account:profile")
    return render(request, "profile.html", {"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        user_name = form.cleaned_data["user_name"]
        password = form.cleaned_data["password"]

        # ALWAYS use create_user
        user = MyUser.objects.create_user(
            email=email,
            user_name=user_name,
            password=password,
            is_active=True,
            is_verify=True
        )

        messages.success(request, "Account created successfully.")
        return redirect("account:login")

    return render(request, "accounts/register.html", {"form": form})



def userlogin(request):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        print("Email:", username)
        print("Password:", password)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:dashboard")
        messages.error(request, "Invalid username/email or password.")

    return render(request, "accounts/login.html")
