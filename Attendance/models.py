import datetime
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128) 
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    face_data = models.BinaryField(null=True, blank=True)
    
    def set_password(self, raw_password):
        """Hashes the password and saves it to the password field."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Checks if the provided password matches the hashed password."""
        return check_password(raw_password, self.password)    
    
class Attendance(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    remark=models.CharField(max_length=50,default="Absent")   
    
    class Meta:
        unique_together = ('student', 'date')