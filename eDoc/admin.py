from django.contrib import admin

from eDoc.models import Patient, Doctor, Specialization

admin.site.register(Patient)

admin.site.register(Specialization)


class DoctorAdminModel(admin.ModelAdmin):
    list_display = ['name', 'contact', 'email', 'address']


admin.site.register(Doctor, DoctorAdminModel)
