from django.db import models


class Service(models.Model):
    servicer_name = models.CharField(max_length=100)
    servicing_name = models.CharField(max_length=100, null=False, blank=False)
    sevicing_cost = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS = [
        ('pending','Pending'),
        ('complete','Completed'),
    ]
    
    status = models.CharField(max_length=25, choices=STATUS, default='pending')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.servicer_name