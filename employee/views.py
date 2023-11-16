from django.shortcuts import render,redirect
from .models import *
# Create your views here.
def home(request):
    return render(request,'index.html')

def employees(request):
    employ=Employees.objects.all()
    categ=category.objects.all()
    context={
        "employees":employ,
        "categorys":categ
    }
    return render(request,'employees.html',context)


def employform(request):
    if (request.method=="POST"):
     name=request.POST.get('name')
     age=request.POST.get('age')
     address=request.POST.get('address')
     phone=request.POST.get('phone')
     mail=request.POST.get('mail') 
     photo=request.FILES.get('photo')
     category_name = request.POST.get('category')
     category_instance = category.objects.get(category_name=category_name)

     Employees.objects.create(
         name=name,
         phone=phone,
         mail=mail,
         address=address,
         photo=photo,
         category=category_instance,
         age=age
     )
     


     return redirect('/employees')
def notice(request):
    return render(request,'notice.html')

def task(request):
    return render(request,'task.html')

def delete_employee(request,id):
      try:
        Employees.objects.get(id=id).delete()

        return redirect('/employees')
      except Exception as e:
          print(e)