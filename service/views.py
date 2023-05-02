from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
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
    return render(request, "service/service_add.html", context)

def service_info(request):
    service = Service.objects.all()
    context = {
        'service' : service,
    }
    return render(request, 'dashboard/service_info.html', context)

# @login_required
def upadate_service(request, service_id):
    service = Service.objects.get(id=service_id)
    form = ServicingForm(instance=service)
    context = {
        "form": form,
    }
    service_inc = Service.objects.get(id=service_id)
    form = ServicingForm(request.POST or None, request.FILES or None, instance=service_inc)
    if form.is_valid():
        form.save()
        return redirect('service-info')
    else:
        form = ServicingForm()
    return render(request, 'service/update.html', context)


# @login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('service-info')
