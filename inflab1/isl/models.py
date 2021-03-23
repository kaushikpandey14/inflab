from django.db import models

# Create your models here.
class general_m(models.Model):
    slabs = models.CharField(max_length=900, default=' ',null=True)
    length = models.CharField(max_length=400, default=' ',null=True)
    breadth = models.CharField(max_length=400, default='8',null=True)
    height = models.CharField(max_length=300, default='8',null=True)
    cost = models.CharField(max_length=15, default=' ',null=True)
    nodes = models.CharField(max_length=15, default=' ',null=True)


    def __str__(self):
        return str(self.slabs)