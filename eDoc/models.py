from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


class Specialization(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    address = models.CharField(max_length=50)
    picture = models.ImageField(null=True, upload_to='profileImages', blank=True)
    description = models.TextField(null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
