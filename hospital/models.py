from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
import datetime


# departments=[('Cardiologist','Cardiologist'),
# ('Dermatologists','Dermatologists'),
# ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
# ('Allergists/Immunologists','Allergists/Immunologists'),
# ('Anesthesiologists','Anesthesiologists'),
# ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
# ]
departments = [
('orthodontist','orthodontist'),
('endodontist','endodontist'),
('maxillofacialSurgeon','maxillofacialSurgeon'),
('prosthodontist','prosthodontist'),
('implotology','implotology'),
('pedodontist','pedodontist'),
('oralmedicine&pathologist','oralmedicine&pathologist'),
('other','other')


]

Patient_type = [
    ('pretreatment','pretreatment'),
    ('Registrationcount','Registrationcount'),
    ('Preauthorisation','Preauthorisation'),
    ('Dischargestate','Dischargestate'),
    ('Claimphase','Claimphase'),
    ('surgery_update','surgery_update')

]



Patient = [
    ('approved','approved'),
    ('pending','pending'),
    ('approvedExcept','approvedExcept'),
    ('other','other'),
    ('caseStartedWithoutApproval','caseStartedWithoutApproval'),
    ('Running','Running'),
    ('compleated','compleated'),
    ('DischargeUpdated','DischargeUpdated'),
    ('DischargeUpdatePending','DischargeUpdatePending'),
    ('needToApply','needToApply'),
    ('claimApplied','claimApplied'),
    ('claimPending','claimPending'),
    ('claimapproved','claimapproved'),
]
status = [
    ('approved','approved'),
    ('pending','pending'),
    ('approvedExcept','approvedExcept'),
    ('other','other'),
    ('caseStartedWithoutApproval','caseStartedWithoutApproval'),
    ('Running','Running'),
    ('compleated','compleated'),
    ('DischargeUpdated','DischargeUpdated'),
    ('DischargeUpdatePending','DischargeUpdatePending'),
    ('needToApply','needToApply'),
    ('claimApplied','claimApplied'),
    ('claimPending','claimPending'),
    ('claimapproved','claimapproved')


]


class LabDetails(models.Model):
    LabId=models.CharField(max_length=200) 
    LabName = models.CharField(max_length=200)
    LabAddress = models.CharField(max_length=200)
    history = HistoricalRecords()
    def __str__(self):
        return self.LabId


class treatmentInfo(models.Model):
    # Patient= models.ForeignKey(Patient,on_delete=models.CASCADE)
    TreatmentCode = models.CharField(max_length=200,null=False)
    TreatmentName = models.CharField(max_length=200,null=False)
    TreatmentCost = models.CharField(max_length=200,null =False)
    history = HistoricalRecords()
    def __str__(self):
        return self.TreatmentName



class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField()
    history = HistoricalRecords()
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)


class his(models.Model):
    user_id = models.ForeignKey('auth.User',null = False,on_delete=models.CASCADE)



class Patient(models.Model):
    #user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100,null=False)
    age = models.PositiveIntegerField()
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    Patient_type_1  = models.CharField(max_length=50,choices=Patient_type)
    status1  = models.CharField(max_length=50,choices=Patient)
    LabDetails = models.ForeignKey(LabDetails,null = True,on_delete=models.CASCADE)
    treatmentInfo = models.ForeignKey(treatmentInfo,null = True , on_delete=models.CASCADE)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    # changed_by = models.ForeignKey(his, null = True,on_delete=models.CASCADE)
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    
    
   
    def __str__(self):
        
        return self.first_name
    


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    history = HistoricalRecords()



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)
    profile_pic= models.ImageField(upload_to='profile_pic/dicharge/',null=True,blank=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
    history = HistoricalRecords()




class test1(models.Model):
    folderName = models.CharField(max_length=100 ,null=False)
    Patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.folderName
    # def __str__(self):
    #     self.Patient

# class test2(models.Model):
#     Patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
#     test = models.ImageField(upload_to='testphotos/test2/', null=True,blank=True)
#     discription = models.CharField(max_length=100 ,null=False)
#     def __str__(self):
#         self.Patient

# class test3(models.Model):
#     Patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
#     test = models.ImageField(upload_to='testphotos/test3/', null=True,blank=True)
#     discription = models.CharField(max_length=100 ,null=False)
#     def __str__(self):
#         self.Patient
# class test4(models.Model):
#     Patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
#     test = models.ImageField(upload_to='testphotos/test4/', null=True,blank=True)
#     discription = models.CharField(max_length=100 ,null=False)
#     def __str__(self):
#         self.Patient    
        
# class names(models.Model):
#     name = models.CharField(max_length=200)
#     testname = models.ForeignKey(test3 ,on_delete=models.CASCADE) 


class testphotos(models.Model):
    test = models.ImageField(upload_to='testphotos/test1/', null=True,blank=True)
    discription = models.CharField(max_length=100 ,null=False)
    type = models.CharField(max_length=100 ,null=False)
    folderName = models.ForeignKey(test1,on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    # def __str__(self):
    #     return self.folderName
        
  





# class LabDetails(models.Model):
#     LabId=models.CharField(max_length=200,null=False) 
#     LabName = models.CharField(max_length=200,null=False)
#     LabAddress = models.CharField(max_length=200,null=False)
    # Patient = models.ForeignKey(Patient,on_delete=models.CASCADE) 


# class priscriptrion(models.Model):

class priscriptrion(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    text = models.CharField(max_length=200,null=False) 
    history = HistoricalRecords()