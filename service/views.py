from django.http import HttpResponse, HttpResponseBadRequest
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
    return render(request, 'service/service_add.html', context)

def service_info(request):
    # current_date = timezone.now().date()  # Get the current date
    # start_of_month = date(current_date.year, current_date.month, 1)  # Calculate the start of the current month

    # monthly_total_cost = Service.objects.filter(date_added__gte=start_of_month) \
    #     .aggregate(total_cost=Sum('sevicing_cost'))['total_cost']

    # print(monthly_total_cost)
    # # 'monthly_total_cost' will contain the sum of 'sevicing_cost' for all services added this month.

    # if monthly_total_cost is not None:
    #     print(f"Monthly total servicing cost: {monthly_total_cost}")
    # else:
    #     print("No services added this month.")


    total_amount = 0
    services = Service.objects.filter(status='pending')
    service = Service.objects.filter(status='complete')
    # for x in services:
    #     total_amount += x.sevicing_cost

    for x in service:
        total_amount += x.sevicing_cost

    context = {
        'services': services,
        'total_amount' : total_amount,
        'service' : service,
    }
    return render(request, 'service/service_info.html', context)
    
def update_status(request, service_id):
    task = Service.objects.get(id=service_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status == 'complete' and task.status == 'pending':
            task.status = new_status
            task.save()
            return HttpResponse()  # Return a success response

    return HttpResponseBadRequest('Invalid request')

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




