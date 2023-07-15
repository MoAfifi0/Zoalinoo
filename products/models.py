from django.db import models
import datetime
from datetime import *

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=7 , decimal_places=2 )
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_active = models.BooleanField( default=True )
    publish_date = models.DateTimeField( default=datetime.now )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-publish_date']