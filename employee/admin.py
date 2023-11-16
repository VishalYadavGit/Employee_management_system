from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(category)
admin.site.register(Employees)
admin.site.register(Notice)