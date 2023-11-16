from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    return render(request,'index.html')

def employees(request):
    employ=Employees.objects.all()
    context={
        "employees":employ
    }
    return render(request,'employees.html',context)
def employform(request):
    return render(request,'task.html')
def notice(request):
    return render(request,'notice.html')

def task(request):
    return render(request,'task.html')