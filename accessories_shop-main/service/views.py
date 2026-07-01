from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ServicingForm
from .models import Service


@login_required(login_url="account:login")
def add_service(request):
    form = ServicingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("service-info")
    return render(request, "service/service_add.html", {"form": form})


@login_required(login_url="account:login")
def service_info(request):
    pending_services = Service.objects.filter(status="pending")
    completed_services = Service.objects.filter(status="complete")
    total_amount = completed_services.aggregate(total=Sum("sevicing_cost"))["total"] or 0

    context = {
        "services": pending_services,
        "service": completed_services,
        "total_amount": total_amount,
    }
    return render(request, "service/service_info.html", context)


@login_required(login_url="account:login")
@require_POST
def update_status(request, service_id):
    task = get_object_or_404(Service, id=service_id)
    new_status = request.POST.get("status")

    if new_status == "complete" and task.status == "pending":
        task.status = new_status
        task.save(update_fields=["status"])
        return HttpResponse()

    return HttpResponseBadRequest("Invalid request")


@login_required(login_url="account:login")
def upadate_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    form = ServicingForm(request.POST or None, instance=service)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("service-info")
    return render(request, "service/update.html", {"form": form})


@login_required(login_url="account:login")
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect("service-info")
