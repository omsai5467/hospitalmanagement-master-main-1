from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,test1,test2,test3,test4
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

# admin.site.register(test_test)
admin.site.register(test1)
admin.site.register(test2)
admin.site.register(test3)
admin.site.register(test4)