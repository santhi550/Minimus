from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
class Items(models.Model):
    url=models.CharField("URL",max_length=1000)
    user_id=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    availability=models.BooleanField(default=False)