from django.shortcuts import render, redirect
from .models import Service
from .forms import ServicingForm

def add_service(request):
    form = ServicingForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('service-info')
    else:
        form = ServicingForm()
    context = {
        'form': form,
    }
    return render(request, "dashboard/service_add.html", context)

def service_info(request):
    service = Service.objects.all()

    context = {
        'service' : service,
    }
    return render(request, 'dashboard/service_info.html', context)