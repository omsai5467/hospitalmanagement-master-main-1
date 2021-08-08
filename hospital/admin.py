from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,test1,testphotos , LabDetails,treatmentInfo  #,test2,test3,test4,names
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
admin.site.register(testphotos)
# admin.site.register(test3)
admin.site.register(treatmentInfo)
admin.site.register(LabDetails)