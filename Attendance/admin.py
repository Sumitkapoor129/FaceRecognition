from django.contrib import admin
from .models import Students,Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date','remark')
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id','face_data')    
# Register your models here.
admin.site.register(Students,StudentsAdmin)
admin.site.register(Attendance,AttendanceAdmin)