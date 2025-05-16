from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


    class Meta:
        db_table = 'customer'
        managed = False # not to create or change this table