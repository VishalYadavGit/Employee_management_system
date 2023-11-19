from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.utils.dateformat import DateFormat
from datetime import date,timedelta
from django.http import Http404
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
     salary=request.POST.get('salary')
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
         age=age,
         salary=salary
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
    employees = Employees.objects.all()
    current_date = date.today()
    start_of_month = current_date.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    all_dates = [start_of_month + timedelta(days=i) for i in range((end_of_month - start_of_month).days + 1)]

    # Create a list of dictionaries to store attendance data for each employee and date
    attendance_data = []
    for employee in employees:
        employee_data = {'employee': employee, 'attendance': []}
        present_count = 0
        for current_date in all_dates:
            attendance_record, created = Attendance.objects.get_or_create(employee=employee, date=current_date)
            employee_data['attendance'].append({'date': current_date, 'status': attendance_record.status})
            if attendance_record.status == 'P':
                present_count += 1  # Increment count for present days
        employee_data['present_count'] = present_count
        employee_data['estimated_salary'] = employee.salary * present_count
        attendance_data.append(employee_data)
        current_month_year = DateFormat(current_date).format('F Y')


    context = {
        'employees': employees,
        'all_dates': all_dates,
        'attendance_data': attendance_data,
        'current_month_year':current_month_year
    }

    return render(request, 'task.html', context)

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

def attendance(request):
    employees=Employees.objects.all()
    return render(request,'attendance.html',{"employees":employees})

def checkattendance(request):
    if request.method=='POST':
        uuid=request.POST.get('uuid')
        aid=request.POST.get('aid')
        if aid=="admin123":
            try:
                new_uuid = uuid[9:]
                new_uuid =int(new_uuid)
                if type(new_uuid)==int:
                    try:
                        if Employees.objects.filter(id=new_uuid).exists():
                            get_employee=Employees.objects.get(id=new_uuid)
                            attendance_record, created = Attendance.objects.get_or_create(employee=get_employee, date=date.today())
                            attendance_record.status = 'P'
                            attendance_record.save()
                            success_url = reverse('attendancesuccess', args=[new_uuid])
                            return redirect(success_url)
                        else:
                            messages.error(request,"Invalid Credentials!!")
                    except(ValueError):
                        messages.error(request,"Invalid Credentials!!")

                        
                else:
                    messages.error(request,"Invalid Credentials!!")
            except ValueError:
                messages.error(request, "Invalid UUID Format!!")
        else:
            messages.error(request, "Invalid Credentials!!")
            return render(request, 'attendance.html')
        
def attendancesuccess(request,new_uuid):
    try:
        print(type(new_uuid))
        
        new_uuid=int(new_uuid)
        print(type(new_uuid))
        instance=Employees.objects.get(id=new_uuid)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message=f"Thank you {instance.name}!,Your Attendance is done on {formatted_datetime}"
        return render(request,'atdsuccess.html',{'message': message})
    except (ValueError, Employees.DoesNotExist):
        raise Http404("Invalid UUID")