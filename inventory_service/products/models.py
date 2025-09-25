from django.db import models

class Product(models.Model):
    id  =  models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    code = models.CharField(max_length=15, unique=True)
    category = models.JSONField()
    price = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} --- > {self.price}/= KES'
    
    class Meta:
        ordering = ["-created_at"]