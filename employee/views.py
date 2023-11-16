from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
# Create your views here.
def home(request):
    employ=Employees.objects.count()
    notice=Notice.objects.count()
    categ=category.objects.count()
    context={
        "employeescount":employ,
        "noticecount":notice,
        "catecount":categ
    }

    return render(request,'index.html',context)

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
    employ=Employees.objects.all()
    notice=Notice.objects.all()
    context={
        "employees":employ,
        "Notices":notice
    }

    return render(request,'notice.html',context)

def task(request):
    return render(request,'task.html')

def delete_employee(request,id):
      try:
        Employees.objects.get(id=id).delete()

        return redirect('/employees')
      except Exception as e:
          print(e)

def noticesend(request):
    if request.method=='POST':
        message=request.POST.get('message')
        receipent=request.POST.get('receipent')
        subject=request.POST.get('subject')
        Notice.objects.create(
            message=message,
            receipent=receipent,
            subject=subject,
        )
        if receipent!="Everybody":
            objectget=Employees.objects.get(name=receipent)
            email=objectget.mail
            mail=f'''
            {email}
            {subject}
            {message}
            '''
            send_mail(receipent,mail,'',[email])

        else:
            allobj=Employees.objects.all()
            for employee in allobj:
                employee_emails = employee.mail
                mail=f'''
                {employee_emails}
                {subject}
                {message}
                '''
                send_mail(receipent,mail,'',[employee_emails])
            
        return redirect('/notice')
