from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.utils.encoding import python_2_unicode_compatible

USER_TYPE = (('DOCTOR', 'DOCTOR'), ('RECEPTIONIST', 'RECEPTIONIST'),)
USER_SPECIALISED = (('EMPLANT', 'EMPLANT'), ('ORTHO', 'ORTHO'), ('SURGERY', 'SURGERY'))
USER_GENDER = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
USER_QUALIFICATION = (('low', 'low'), ('middle', 'middle'), ('high', 'high'))
TIMECHOSES = [(dt.time(9, 0), "9 a.m."), (dt.time(10, 0), "10 a.m."), (dt.time(11, 0), "11 a.m."),(dt.time(14, 0), "2 p.m."), (dt.time(15, 0), "3 p.m.")]

@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=15, choices=USER_TYPE, default='PATIENT')
    user_addr = models.CharField(max_length=155, null=True)
    user_mobile = models.CharField(max_length=15, null=True)
    user_hire_date = models.DateField(blank=True, null=True)
    user_dob = models.DateField(blank=True, null=True)
    user_specialised = models.CharField(max_length=15, choices=USER_SPECIALISED, blank=True, null=True)
    user_sex = models.CharField(max_length=10, choices=USER_GENDER, default='MALE')
    user_qualification = models.CharField(max_length=100, choices=USER_QUALIFICATION, default='middle')
    user_bloodgroup = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)


class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    bloodgroup = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=USER_GENDER, default='MALE')
    age = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='treat_doctor', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    token = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)
    dental_position = models.CharField(max_length=50, blank=True, null=True)
    dental_test = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Appoiment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='app_doctor', on_delete=models.CASCADE)
    token = models.IntegerField()
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(choices=TIMECHOSES,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.patient.name, self.doctor.username)

    class Meta:
        ordering = ('date',)


class Bill(models.Model):
    date = models.DateField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='bill_doctor', on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.patient)
