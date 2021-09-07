
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import JsonResponse , QueryDict
from django.core import serializers
from zipfile import ZipFile
from wsgiref.util import FileWrapper
import os
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    num = Group.objects.all().count()
    print(num)
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html',{'num':num})


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')




def admin_signup_view(request):
    n = Group.objects.all().count()
    if n > 0 :
        return HttpResponse('😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁🤣🤣🤣🤣🤣😂😂😂😘😘🤷‍♀️🤷‍♀️🤦‍♂️🤦‍♀️😎🎶😢💖😜')
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    #userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'patientForm':patientForm}
    if request.method=='POST':
        #userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if  patientForm.is_valid():
            print("is valid")
            #user=userForm.save()
           # user.set_password(user.password)
            #user.save()
            patient=patientForm.save(commit=False)
            #patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            #my_patient_group = Group.objects.get_or_create(name='PATIENT')
            #my_patient_group[0].user_set.add(user)
            print("not valid")    
            return HttpResponse('taken your appointment request ')
        return HttpResponse(" please fill correct details")    

    return render(request,'hospital/patientsignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update').count()
    print(Surgery_update)


    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    print(pretreatment)

    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    #user=models.User.objects.get(id=patient.user_id)
    #user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    #user=models.User.objects.get(id=patient.user_id)

    #userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(instance=patient)
    mydict={'patientForm':patientForm}
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        symptoms = request.POST['symptoms']
        mobile = request.POST['mobile']
        address = request.POST['address']
        patient.first_name=first_name
        patient.last_name=last_name
        patient.symptoms=symptoms
        patient.mobile=mobile
        patient.address=address
        patient.save()
        return redirect('admin-view-patient')
        print('patient saved')
        #userForm=forms.PatientUserForm(request.POST,instance=user)
        # patientForm=forms.PatientForm(request.POST,instance=patient)
        # if   patientForm.is_valid():
        #     #user=userForm.save()
        #     #user.set_password(user.password)
        #     #user.save()
        #     patient=patientForm.save(commit=False)
            
        #     patient.assignedDoctorId=request.POST.get('assignedDoctorId')
        #     patient.save()
            
    return render(request,'hospital/admin_update_patient.html',context=mydict)


import base64


import os
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    print(request.user)
   # userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'patientForm':patientForm}
    if request.method=='POST':
        img  = request.POST['img']
        a = img[22:]
        # imgdata = base64.b64decode(a)
        # filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
        # with open(filename, 'wb') as f:
        #     f.write(imgdata)
        from datetime import datetime
        now = str(datetime.now())

        print(now)


   


        # Treatment_info = request.POST['Treatment_info']
        first_name = request.POST['first_name']
        address = request.POST['address']
        symptoms = request.POST['symptoms']
        status = request.POST['status']
        
        assignedDoctorId = request.POST['assignedDoctorId']
        #patient.assignedDoctorId=request.POST.get('assignedDoctorId')
        last_name = request.POST['last_name']
        mobile = request.POST['mobile']
        Patient_type_1 = request.POST['Patient_type_1']
        status1 = request.POST['status1']
        import base64, secrets, io
        from PIL import Image
        from django.core.files.base import ContentFile
        _format, _dataurl       = img.split(';base64,')
        _filename, _extension   = secrets.token_hex(30), _format.split('/')[-1]

        file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
        
        from PIL import Image, ImageDraw
        from PIL import Image, ImageDraw, ImageFont

        image = Image.open(file)
        width, height = image.size 
        draw = ImageDraw.Draw(image)
        text = now
        textwidth, textheight = draw.textsize(now)
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        draw.text((x, y), text)

        image.save('devnote.png')
        image = Image.open('devnote.png')
        im = open('devnote.png','rb')
        str1=  base64.b64encode(im.read())
        modImage = ContentFile( base64.b64decode(str1), name=f"{_filename}.{_extension}")
        
        # import os
        # os.remove('devnote.png')       
        #img2 = ContentFile(img1.save('om.jpg'), name=f"{_filename}.{_extension}")
        obj, p = models.Patient.objects.get_or_create(
            first_name =first_name,
            address = address,
            symptoms =symptoms,
            status ='True',
            profile_pic = modImage,
            last_name =last_name,
            mobile = mobile,
            Patient_type_1 =Patient_type_1,
            assignedDoctorId = assignedDoctorId,
            status1= status1,
            age = request.POST['age']
           

                                                          )
        
        

        # print(spit)
        
        return render(request,'hospital/admin_add_patient.html',context=mydict)
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    #user=models.User.objects.get(id=patient.user_id)
    #user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required()
# @user_passes_test(is_admin)
def discharge_patient_view(request,pk):

    # p = models.Patient.objects.get(id=pk)
    import datetime
    now = datetime.datetime.now()
                   
    
    from datetime import datetime,date

    patient=models.Patient.objects.get(id=pk)
    print(type(patient.admitDate))
    now = patient.admitDate
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))
    day = int(now.strftime("%d"))
    t1 = date(year = year , month = month , day = day)
    up = datetime.today()
    year1 = int(up.strftime("%Y"))
    month2 = int(up.strftime("%m"))
    day2 = int(up.strftime("%d"))
    t2 = date(year = year1,month=month2,day= day2)
    t3 = t2 - t1

    
    print(datetime.now())

    print(t1)
    print(t3)
    
    days=t3 #2 days, 0:00:00
    print(type(patient.admitDate))
    assignedDoctor=models.User.objects.get(id=patient.assignedDoctorId)
    # print(assignedDoctor[0].department)
    dep = models.Doctor.objects.get(user = assignedDoctor  )
    print(dep.department)

    d=days.days # only how many day that is 2
    preauthapproved = patient.history.filter(Patient_type_1 = "Preauthorisation",status1='approved')
    Surgery_updateRunningTime = patient.history.filter(Patient_type_1 = "surgery_update",status1 = 'Running')
    Surgery_updateCompleted = patient.history.filter(Patient_type_1 = "surgery_update",status1 = 'compleated')
        


    patientDict={
        'p':patient,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor.first_name,
        'preauthapproved':preauthapproved,
        'Surgery_updateRunningTime':Surgery_updateRunningTime,
        'Surgery_updateCompleted':Surgery_updateCompleted,
        'dep':dep

    }
    patient.delete()
    return render(request,"invoice.html" ,context=patientDict)
    # t1 = models.test1.objects.all().filter(Patient = p).count()
    # t2 = models.test2.objects.all().filter(Patient = p).count()
    # t3 = models.test3.objects.all().filter(Patient = p).count()
    # t4 = models.test4.objects.all().filter(Patient=p).count() 
    # t1 = models.testphotos.objects.all().filter(Patient=p).count()
    
    # print('hi')
    
    # if request.method == 'POST':
    #     feeDict ={
    #         'roomCharge':int(request.POST['roomCharge'])*int(d),
    #         'doctorFee':request.POST['doctorFee'],
    #         'medicineCost' : request.POST['medicineCost'],
    #         'OtherCharge' : request.POST['OtherCharge'],
    #         'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
    #     }
        
    #     patientDict.update(feeDict)
    #     # for updating to database patientDischargeDetails (pDD)
    #     # import base64, secrets, io
    #     # # from PIL import Image
    #     # from django.core.files.base import ContentFile
    #     # # #_format, _dataurl       = img.split(';base64,')
    #     # # _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]
    #     # im = open(patient.profile_pic,'rb')
    #     # print(im.read())
    #     # # str1=  base64.b64encode(im.read())
    #     # # modImage = ContentFile( base64.b64decode(str1), name=f"{patient.first_name}.png")

    #     # # #file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
    #     # import base64
    #     # a=  'static\profile_pic\PatientProfilePic\om.png'
    #     # with open(a, "rb") as img_file:
    #     #     my_string = base64.b64encode(img_file.read())
    #     #     print(my_string)
        
    #     pDD=models.PatientDischargeDetails()
    #     pDD.patientId=pk
    #     pDD.patientName=patient.first_name
    #     pDD.profile_pic=patient.profile_pic
    #     print(patient.profile_pic)

    #     pDD.assignedDoctorName=assignedDoctor[0].first_name
    #     pDD.address=patient.address
    #     pDD.mobile=patient.mobile
    #     pDD.symptoms=patient.symptoms
    #     pDD.admitDate=patient.admitDate
    #     pDD.releaseDate=date.today()
    #     pDD.daySpent=int(d)
    #     pDD.medicineCost=int(request.POST['medicineCost'])
    #     pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
    #     pDD.doctorFee=int(request.POST['doctorFee'])
    #     pDD.OtherCharge=int(request.POST['OtherCharge'])
    #     pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
    #     pDD.save()
    # # patient=models.Patient.objects.get(id=pk)
    #     patient.delete()
    #     print('patient deleted')
            

    #     return render(request,'hospital/patient_final_bill.html',context=patientDict)
    #     return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})





            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


@login_required
def pretreatment(request):
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True).count()
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    patients = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True)
    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    'patients':patients
    #context=mydict
    }
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    # from datetime import datetime
    for p in patients:
        # print(datetime.now() )
        d = str(now - p.updated)
        e = d
        print(e.split())
        p.updated = 30 - int(e[0])
        print(type(d))

    

    return render(request,'hospital/pretreatment.html',context=mydict)
@login_required
def Registrationcount(request):
    today = datetime.now()
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True).count()

    patients = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True)
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients1=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()


    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    patients2 = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True)
    mydict={

    'Surgery_update':Surgery_update,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    'from_date': today,
    'source':'Registrationcount',
    # 'color': 'red'

    #context=mydict
    }
    days = []
    # patients = models.Patient.objects.all().filter(Patient_type_1='Registrationcount')
    print(patients)

    return render(request,'hospital/Registrationcount.html',context=mydict)

@login_required
def surgery(request):

    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    patients = models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True)
    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    'patients':patients
    #context=mydict
    }
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    # from datetime import datetime
    for p in patients:
        # print(datetime.now() )
        d = str(now - p.updated)
        e = d
        print(e.split())
        p.updated = 30 - int(e[0])
        print(type(d))

    

    return render(request,'hospital/surgery.html',context=mydict)
@login_required
def Registrationcount(request):

    patients = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True)
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients1=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    patients2 = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True)
    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,

    #context=mydict
    }
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    # from datetime import datetime
    for p in patients:
        # print(datetime.now() )
        d = str(now - p.updated)
        e = d
        print(e.split())
        p.updated = 30 - int(e[0])
        print(type(d))

    return render(request,'hospital/Registrationcount.html',context=mydict)










@login_required
def Preauthorisation(request):

    patients = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True)
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients1=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    patients2 = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True)
    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    'patients':patients,
    
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    
    #context=mydict
    }
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    # from datetime import datetime
    for p in patients:
        # print(datetime.now() )
        d = str(now - p.updated)
        e = d
        print(e.split())
        p.updated = 30 - int(e[0])
        print(type(d))
    return render(request,'hospital/Preauthorisation.html',context=mydict)
@login_required
def Dischargestate(request):
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='Surgery_update',status=True).count()

    patients = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True)
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients1=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()
    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    'patients':patients
    #context=mydict
    }
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    # from datetime import datetime
    for p in patients:
        # print(datetime.now() )
        d = str(now - p.updated)
        e = d
        print(e.split())
        p.updated = 30 - int(e[0])
        print(type(d))
    
    return render(request,'hospital/Dischargestate.html',context=mydict)  
@login_required
def Claimphase(request):
    Surgery_update =  models.Patient.objects.all().filter(Patient_type_1='surgery_update',status=True).count()

    patients = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True)
    pretreatment = models.Patient.objects.all().filter(Patient_type_1='pretreatment',status=True).count()
    doctors=models.Doctor.objects.all().order_by('-id')
    patients1=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    Registrationcount = models.Patient.objects.all().filter(Patient_type_1='Registrationcount',status=True).count()
    Preauthorisation = models.Patient.objects.all().filter(Patient_type_1='Preauthorisation',status=True).count()
    Dischargestate = models.Patient.objects.all().filter(Patient_type_1='Dischargestate',status=True).count()
    Claimphase = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status=True).count()

    mydict={
    'Surgery_update':Surgery_update,
    'doctors':doctors,
    
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    'pretreatment':pretreatment,
    'Registrationcount':Registrationcount,
    'Preauthorisation':Preauthorisation,
    'Dischargestate':Dischargestate,
    'Claimphase':Claimphase,
    'patients':patients
    #context=mydict
    }
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    # from datetime import datetime
    for p in patients:
        # print(datetime.now() )
        d = str(now - p.updated)
        e = d
        print(e.split())
        p.updated = 30 - int(e[0])
        print(type(d))
    return render(request,'hospital/Claimphase.html',context=mydict)
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



@login_required
def test(request,pk):

    patient=models.Patient.objects.get(id=pk)
    p=models.Patient.objects.get(id=pk)
    d = models.Doctor.objects.get(user = p.assignedDoctorId)
    
    patientForm=forms.PatientForm(instance=patient)
  #  Patient_type_1=Claimphase&status1=compleated
    mydict={'patientForm':patientForm,'patient':patient}
    if request.method=='POST':
        patient=models.Patient.objects.get(id=pk)
        Patient_type = request.POST['Patient_type_1']
        status1 = request.POST['status1']
        #        p = models.Patient.objects.get_or_create(

        #p = models.Patient.objects.update_or_create(id=pk,Patient_type_1=Patient_type,status1=status1)
        patient.Patient_type_1 = Patient_type
        patient.status1 = status1
        patient.save()
        print(Patient_type)
        # for i in range(20):
        return render(request,'hospital/overview_patient.html',{'p':p,'d':d})


        #userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,instance=patient)
        if   patientForm.is_valid():
            
            #user=userForm.save()
            #user.set_password(user.password)
            #user.save()
            
            
            
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/test1.html',context=mydict)

def overView(request,pk):
    print(pk)
    p = models.Patient.objects.get(id = pk)
    d = models.Doctor.objects.get(user= p.assignedDoctorId)
    # overView = models.treatmentInfo.objects.all().filter(Patient= p)
    # print(overView)
    LabDetails = models.LabDetails.objects.all()
    TreatmentInfo = models.treatmentInfo.objects.all()
    # try:
    # patientLab = models.LabDetails.objects.get(id = p.LabDetails)
    # patientTreatmentInfo = models.treatmentInfo.objects.get(id = p.treatmentInfo)
        
    # except:
    patientLab = 'none'
    patientTreatmentInfo = 'none'
    return render(request,'hospital/overview_patient.html',{'p':p,'d':d, 'LabDetails':LabDetails,'TreatmentInfo':TreatmentInfo ,'patientLab':patientLab,'patientTreatmentInfo':patientTreatmentInfo   })





def update(request, pk):
    pass
# added python 3.9 dashboard update
#addddd
@login_required
def search(request):
    search = request.POST['id']
    try:
        p = models.Patient.objects.get(id=search)
        return render(request,'hospital/search.html',{'p':p})
    except:
        html = "<html><body><script> alert('Not found patient')  </script></body></html>" 
        return HttpResponse(html)
        # return HttpResponse('<script> patient not found</script>')


@login_required
def folders(request,pk):
    if login_required(login_url='adminlogin'):
        print(bool(login_required(login_url='patientlogin')))
        global patient_id
        # patient_id= pk.get(id=patient_id)
        # names = models.tes
        # p = models.Patient.objectst1.objects.all().filter(Patient = p)
        # return render(request,'hospital/folder.html',{'folderName':names})
        patient_id= pk
        p = models.Patient.objects.get(id=patient_id)
        names = models.test1.objects.all().filter(Patient = p)
        return render(request,'hospital/folder.html',{'folderName':names})
    return HttpResponse('haaaa')
@login_required
@csrf_exempt
def createfolder(request):
    

    if request.method == "POST":
        patient12 = models.Patient.objects.get(id=patient_id)
        # names_Rename = models.test1.objects.all().filter(Patient = patient12)
        # names_Rename.folderName = request.POST['folderId']
        reName = models.test1.objects.get(id = request.POST['folderId'] )
        reName.folderName = request.POST['Name']
        reName.save()




        
        names = models.test1.objects.all().filter(Patient = patient12)

        return render(request,'hospital/folder.html',{'folderName':names})



    p = models.Patient.objects.get(id=patient_id)
    folderName = request.GET['folderName']
    t = models.test1.objects.get_or_create(Patient = p,folderName = folderName)
    names = models.test1.objects.all().filter(Patient = p)
    # t.folderName 
    
    print(folderName)
    return render(request,'hospital/folder.html',{'folderName':names})
@login_required
@csrf_exempt
def DeleteFolder(request):
    if request.method == "POST":
        d = models.test1.objects.get(id = request.POST['ZZid'])
        d.delete()
        return JsonResponse({'hi':"HI"},safe=False)

# def images2(request):
#     if request.method == 'POST':
#         v = request.POST['test2']
#         p = models.test2.objects.get(id=v)
#         p.delete()
#         print('deleted')
#         return redirect('images2')
    
#     print(patient_id)
#     p = models.Patient.objects.get(id=patient_id)
#     t = models.test2.objects.all().filter(Patient = p)
#     print(p.first_name)
#     mydict = {'p':p,'t':t}
#     return render(request,'hospital/gallerytest2.html',context=mydict)
# @login_required
# def images1(request):
#     print(patient_id)
#     p = models.Patient.objects.get(id=patient_id)
#     t = models.test1.objects.all().filter(Patient = p)
#     mydict = {'p':p,'t':t}
#     return render(request,'hospital/gallerytest1.html',context=mydict)
# @login_required
# def images3(request):
#     print(patient_id)
#     if request.method == 'POST':
#         v = request.POST['test2']
#         p = models.test3.objects.get(id=v)
#         p.delete()
#         print('deleted')
#         return redirect('images3')
#     p = models.Patient.objects.get(id=patient_id)
#     t = models.test3.objects.all().filter(Patient = p)
#     mydict = {'p':p,'t':t}
#     return render(request,'hospital/gallerytest3.html',context=mydict)
# @login_required
# def images4(request):
#     print(patient_id)
#     if request.method == 'POST':
#         v = request.POST['test2']
#         p = models.test4.objects.get(id=v)
#         p.delete()
#         print('deleted')
#         return redirect('images4')
#     p = models.Patient.objects.get(id=patient_id)
#     t = models.test4.objects.all().filter(Patient = p)
#     mydict = {'p':p,'t':t}
#     return render(request,'hospital/gallerytest4.html',context=mydict)



@login_required
def test_patient(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/patient_test.html',{'patients':patients})
@login_required
def testing_patient(request,pk):
    global upload_id
    upload_id = pk
    return render (request,'testing_of_patient.html')
@login_required
def gallery_photos(request,pk):
    global user_id
    user_id = pk
    p = models.Patient.objects.get(id=patient_id)
    test = models.test1.objects.get(id = pk)
    a = models.testphotos.objects.all().filter(Patient=p,folderName=test )
    return render(request,'hospital/gallerytest1.html',{'a':a,'id':pk})
@login_required
def uploadImage(request):
    if request.method == 'POST':
        id_om = request.POST['idim']
        image_im = request.FILES['image_01']
        type_file = request.POST['fav_language']
        dis = request.POST['dis']
        p = models.Patient.objects.get(id=patient_id)
        ts = models.test1.objects.get(id=id_om)
        up = models.testphotos.objects.get_or_create(Patient = p,test= image_im,discription = dis,folderName= ts,type = type_file)
        # return redirect(f'gallery_photos/{patient_id}')
        test = models.test1.objects.get(id = user_id)
        a = models.testphotos.objects.all().filter(Patient=p,folderName=test )
        return render(request,'hospital/gallerytest1.html',{'a':a,'id':user_id})
def de(request):
    id = request.GET['btnSubmit'] 
    a = models.testphotos.objects.get(id = id)
    a.delete()
    html = "<html><body><script> alert('REFRESH the page')  </script></body></html>" 
    return HttpResponse(html)

@login_required
def upload_test(request):
    patient = models.Patient.objects.get(pk=upload_id)
    if request.method =='POST':
        test = request.POST['test']
        dis = request.POST['w3review']
        photo = request.POST['photo']
        from datetime import datetime
        now = str(datetime.now())
        import base64, secrets, io
        from PIL import Image
        from django.core.files.base import ContentFile
        _format, _dataurl       = photo.split(';base64,')
        _filename, _extension   = secrets.token_hex(30), _format.split('/')[-1]

        file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
        
        from PIL import Image, ImageDraw
        from PIL import Image, ImageDraw, ImageFont

        image = Image.open(file)
        width, height = image.size 
        draw = ImageDraw.Draw(image)
        text = now
        textwidth, textheight = draw.textsize(now)
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        draw.text((x, y), text)

        image.save('devnote.png')
        image = Image.open('devnote.png')
        im = open('devnote.png','rb')
        str1=  base64.b64encode(im.read())
        file_name = patient.first_name + f'{patient.id}'
        modImage = ContentFile( base64.b64decode(str1), name=f"{file_name}.{_extension}")
        if test == 'test1':
            
            p = models.test1.objects.get_or_create(Patient = patient,test= modImage,discription = dis)
            
        elif test == 'test2':
            print('got Test2')
            p = models.test2.objects.get_or_create(Patient = patient,test= modImage,discription = dis) 
        elif test == 'test_3':
            print('test3')
            p = models.test3.objects.get_or_create(Patient = patient,test= modImage,discription = dis)
        elif test == 'test_4':
            print('test4')
            p = models.test4.objects.get_or_create(Patient = patient,test= modImage,discription = dis)
            
       
        print('test finished')        
       
        html = "<html><body><script> alert('uploaded......')  </script></body></html>" 
        return HttpResponse(html)
    


@login_required
def Discharge_update(request):
    p = models.Patient.objects.all().filter(Patient_type_1='Dischargestate')
    return render(request,'Discharge_update.html',{'patients':p})




@login_required
def Claim_update_pending(request):
    p = models.Patient.objects.all().filter(Patient_type_1='Claimphase',status1='claimPending')
    return render(request,'claimupdate.html',{'p':p})

@login_required
def deletePhoto(request,pk):
    p = models.test1.objects.get(id=pk)
    p.delete()
    return redirect('images1')
    
    
@login_required
def delete(request,pk):
    p = models.test2.objects.get(id=pk)
    p.delete()
    return redirect('images2')




    # path('update_doctor/<int:pk>',views.update_doctor, name = 'update_doctor'),
@login_required(login_url='doctorlogin')
def update_doctor(request,pk):
    print(login_required(login_url='doctorlogin'))
    print(request.user)
    patient=models.Patient.objects.get(id=pk)
    
    patientForm=forms.PatientForm(instance=patient)
  #  Patient_type_1=Claimphase&status1=compleated
    mydict={'patientForm':patientForm,'patient':patient}
    if request.method=='POST':
        patient=models.Patient.objects.get(id=pk)
        Patient_type = request.POST['Patient_type_1']
        status1 = request.POST['status1']
        #        p = models.Patient.objects.get_or_create(

        #p = models.Patient.objects.update_or_create(id=pk,Patient_type_1=Patient_type,status1=status1)
        patient.Patient_type_1 = Patient_type
        patient.status1 = status1
        patient.save()
        print(Patient_type)
        # for i in range(20):
       
        return redirect('doctor-view-patient')
       
           


        #userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,instance=patient)
        if   patientForm.is_valid():
            
            #user=userForm.save()
            #user.set_password(user.password)
            #user.save()
            
            
            
            patient.save()
            return redirect('doctor-view-patient')
    return render(request,'hospital/doctor_update_patient.html',context=mydict)



@csrf_exempt
@login_required
def lab(request):
    
    # print(details)
    if request.method == 'POST':
        # p = models.Patient.objects.get(id= request.POST.get('PatientId',False))

        obj,lab = models.LabDetails.objects.get_or_create(LabId=request.POST['LabID'],LabName=request.POST['LabName'],LabAddress=request.POST['LabAddress'])
        # return JsonResponse(model_to_dict(obj),safe = False)
        return JsonResponse({'a':'a'},safe = False)
    return render(request,'hospital/Lab_Details.html')
    



@csrf_exempt
@login_required
def getLab(request):
    # id = request.GET['PatientId']
    # p = models.Patient.objects.get(id = id)
    r = models.LabDetails.objects.all()
    # data = [r]

    
    data= serializers.serialize("json", models.LabDetails.objects.all(),fields=('LabId','LabName','LabAddress'))
    
    return JsonResponse({'data':data},safe=False)



@csrf_exempt
@login_required
def priscriptrion(request):
    patientId = request.POST['id']
    text = request.POST['text']
    # p = models.Patient.objects.get(id = patientId)
    o = models.priscriptrion.objects.get_or_create(Patient = p,text = text)
    return JsonResponse({'message':'saved'})


@csrf_exempt
@login_required
def download(request):
    # import zipfile
    
    # image_path = settings.MEDIA_ROOT+ product_image_url[6:]
    p = models.Patient.objects.get(id = patient_id)
    test = models.test1.objects.get(id = request.GET['folder_id'])
    a = models.testphotos.objects.all().filter(Patient=p,folderName=test )


    from django.http import HttpResponse
    ZIPFILE_NAME = 'pybites_codesnippets.zip'
    # file_name = f"{}.zip"
    # response = HttpResponse(content_type='application/zip')
    # file = test.folderName
    with ZipFile('export.zip', 'w') as export_zip:
        for i in a:
            image_path = i.test.path
            # im = 
            # settings.MEDIA_ROOT+
            export_zip.write(image_path, '{0}.png'.format(i.discription))
    # response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'        
    wrapper = FileWrapper(open('export.zip', 'rb'))
    content_type = 'application/zip'
    content_disposition = 'attachment; filename={0}.zip'.format(test.folderName)

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = content_disposition
    return response







# p = models.Patient.objects.get(id=patient_id)
#     test = models.test1.objects.get(id = pk)
#     a = models.testphotos.objects.all().filter(Patient=p,folderName=test )
#     return render(request,'hospital/gallerytest1.html',{'a':a,'id':pk})
# @csrf_exempt
@login_required
def SaveChanges(request):
    p = models.Patient.objects.get(id = request.GET['PatientId'])

    p.first_name = request.GET['FirstName']
    p.last_name = request.GET['LastName']
    p.mobile = request.GET['PhoneNumber']
    p.address = request.GET['Address']
    L = 'hi'
    t = 'hi'
    if request.GET['LabId'] != 0:
        # global Lab
        Lab = models.LabDetails.objects.get(id = request.GET['LabId'])
        p.LabDetails = Lab
        Labb= serializers.serialize("json",[Lab] )
        # print(L)
        print('came lab')
    if request.GET['T'] != 0:
        # global tr
        tr = models.treatmentInfo.objects.get(id = request.GET['T'])
        p.treatmentInfo = tr
        t = serializers.serialize("json",[tr] )
        print('cam t')
    p.save()
    # data= models.Patient.objects.get(id= request.GET['PatientId'])
    obj = models.Patient.objects.get(id= request.GET['PatientId'])
    data = serializers.serialize("json",[obj] )
    L = serializers.serialize("json",[obj] )
    # print(Labb)
    h= p.history.all()
    for i in  h:
        print(i.first_name,i.updated,i.Patient_type_1)
    # p._change_reason 
    print(h)

    return JsonResponse({'data':data,'L':L,"T":t,'Labb':Labb},safe=False)





@login_required
def AddOpereations(request):
    return render(request,'AddLabDetails.html')


@csrf_exempt
@login_required
def TreatmentInfo(request):
    if request.method == 'POST':
        x = models.treatmentInfo.objects.get_or_create(TreatmentCode = request.POST['TreatmentId'],TreatmentName = request.POST['TreatmentName'],TreatmentCost=request.POST['TreatmentCost'])
        return JsonResponse({'hi':'saved'})
    return render(request,'Treatmentinfo.html')

@login_required
@csrf_exempt
def showTreatments(request):
    if request.method == "POST":

        t = models.treatmentInfo.objects.get(id = request.POST['TreatmentId'])
        t.delete()
        return JsonResponse({"msg":'saved'},safe=False)

    y = models.treatmentInfo.objects.all()
    data= serializers.serialize("json",y )
    return JsonResponse({'data':data},safe=False)
