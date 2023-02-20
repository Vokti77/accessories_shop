from django.db import models


class Service(models.Model):
    servicer_name = models.CharField(max_length=100)
    servicing_name = models.CharField(max_length=100, null=False, blank=False)
    sevicing_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.servicer_name