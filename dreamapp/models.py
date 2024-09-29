from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField( max_length=122)
    email= models.CharField( max_length=122)
    phone= models.CharField( max_length=122)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField( max_length=122)
    gender= models.CharField( max_length=122)
    address= models.TextField()
    age = models.IntegerField()
    age_type = models.CharField(max_length=122)
    phone = models.CharField(max_length=14)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField( max_length=122)
    number_of_doctors = models.IntegerField()
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField( max_length=122)
    positions = models.CharField( max_length=122)
    doctor_fees = models.IntegerField()
    department_name= models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    education = models.TextField()

    def __str__(self):
        return self.name

class Rooms(models.Model):
    room_charge = models.IntegerField()
    room_type =  models.TextField()
    room_desc = models.TextField()

    def __str__(self):
        return self.room_type


class Appointment (models.Model):
    doctor_name = models.TextField()
    patient_name = models.TextField()
    apppointment_date = models.TextField()

class Admit(models.Model):
    name = models.TextField(default='shubham')
    room_type = models.TextField()
    admit_date = models.DateField()

class Discharge(models.Model):
    name = models.TextField(default='shubham')
    date = models.DateField()
    
