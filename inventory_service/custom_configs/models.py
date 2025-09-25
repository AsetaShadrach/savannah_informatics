from django.db import models

class CustomConfigs(models.Model):
    id  =  models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} --- > {self.value}/= KES'
    
    class Meta:
        ordering = ["name"]