from django.db import models
from django.contrib.auth.models import User
import uuid

class category(models.Model):
    category_name=models.CharField(max_length=50)


    def __str__(self):
        return self.category_name

class Employees(models.Model):
    name=models.CharField(max_length=100)
    mail=models.EmailField(max_length=254,default="abc@gmail.com")
    age=models.IntegerField()
    phone=models.IntegerField(default="234234234")
    salary=models.IntegerField(default=2000)
    photo=models.ImageField()
    address=models.CharField(max_length=150)
    category=models.ForeignKey(category,on_delete=models.CASCADE,related_name="employcate")
    
    def __str__(self):
        return self.name
    
class Notice(models.Model):
    created_at = models.DateField(auto_now_add=True)
    receipent=models.CharField(max_length=50)
    subject=models.CharField(max_length=150)
    message=models.CharField(max_length=400)

class Attendance(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, default='A')  # Default to 'A' for Absent

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

