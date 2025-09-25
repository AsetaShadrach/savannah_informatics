from django.db import models
from customers.models import Customer

class Order(models.Model):
    id  =  models.AutoField(primary_key=True)
    order_ref = models.CharField(max_length=20, editable=False)
    order_details = models.JSONField()
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT)
    total =  models.FloatField(blank = False, default=0)
    status =  models.CharField(max_length=10, default="PENDING")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order_ref} made by {self.customer}'
    
    class Meta:
        ordering = ["-created_at"]


