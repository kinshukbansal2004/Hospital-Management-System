from datetime import date

# Create your views here.
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from dreamapp.models import *

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

listf = {}

@csrf_exempt
def success(request):
    listf['send']=True
    listf['sen']=False
    listf['mssg']=True

    return render(request,'bill.html',context=listf)

@csrf_exempt
def success1(request):
    h1list['send']=True
    h1list['sen']=False
    h1list['mssg']=True
    return render(request,'receipt.html',context=h1list)
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:

			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = int(bill)*100 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment

					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()


def index(request):
    return render(request,'a1.html')

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email= request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        submit = Feedback(name= name , email= email, phone = phone , desc = desc , date = date.today())
        submit.save()
        return render (request,'a1.html')

    return render (request,'submit.html')

def emergency(request):
    return render(request,'emergency.html')
h1list = {}
def appointment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        doctor = request.POST.get('doctor')
        doc_name = ""
        for i in range(20):
            if doctor[i]==' ':
                break
            else:
                doc_name+=doctor[i]
        print(doc_name)
        gender = request.POST.get('gender')
        date = request.POST.get('date')
        address = request.POST.get('address')

        s = Patient(name=name,phone=phone,age=age,gender=gender,address=address)
        d = Appointment(doctor_name=str(doc_name),patient_name=name,apppointment_date=str(date))
        s.save()
        d.save()
        web2 = Doctor.objects.all()
        for y in web2:
            if(y.name==doc_name):
                web=y
                break
        context ={'sd':s,'sd1':d,'sd3':web}
        currency = 'INR'
        amount =    web.doctor_fees
        amount = amount*100
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
	    												currency=currency,
	    												payment_capture='0'))

        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['send']=False
        context['sen']=True
        for key, value in context.items():
            h1list[key] = value
        return render (request,'receipt.html',context=context)
    weblist = Doctor.objects.all()
    weblist2 = Department.objects.all()
    dict1 = {'sd': weblist,'sd2':weblist2}
    return render(request,'appointment.html',context=dict1)

def patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        patient_list = Patient.objects.all()
        appointment_list = Appointment.objects.all().order_by('-apppointment_date')
        dict = {1:1}
        listd =[]
        for j in appointment_list:
            if j.patient_name == name:
                listd.append(j)
        dict['sd1']=listd
        c=0
        for y in patient_list:
            if y.name == name and y.phone == phone:
                c=1
                dict['sd'] = y

        if c:
            return render(request,'afterlogin.html',context=dict)
        else:
            return render (request,'patient_login.html',context={'send':True})

    return render(request,'patient_login.html',context={'send':False})

def doctor(request):
    if request.method == "POST":
        name = request.POST.get('name')
        id = request.POST.get('id')
        doctor_list = Doctor.objects.all()
        appointment_list = Appointment.objects.all().order_by('-apppointment_date')
        list1 =[]
        for j in appointment_list:
            if j.doctor_name == name:
                list1.append(j)
        dict = {'sd2':list1}

        for y in doctor_list:
            if y.id == int(id) and y.name == name:
                dict['sd'] =y
                return render(request,'afterlogind.html',context=dict)

        return render (request,'doctor_login.html',context={'send':True})

    return render(request,'doctor_login.html',context={'send':False})

def rooms(request):
    roomlist = Rooms.objects.all()

    dict = {'sd': roomlist}
    return render(request,'rooms.html',context = dict)

def contacts(request):
    return render(request,'contacts.html')

def admit(request):
    if request.method == "POST":
        name=request.POST.get('name')
        date = request.POST.get('date')
        room = request.POST.get('room')
        s = Admit(name=name,admit_date=date,room_type=room)
        s.save()
        return render(request,'a1.html')
    x = Rooms.objects.all()
    # x = set()
    # for y in roomlist:
    #     x.add(y.room_type)
    # print(x)
    dict = {'sd': x}
    return render(request,'admit.html',context=dict)

def discharge(request):
    if request.method == "POST":
        name=request.POST.get('name')
        date = request.POST.get('date')
        s = Discharge(name=name,date=date)
        s.save()
        y = Admit.objects.all()
        k = Discharge.objects.all()
        room = Rooms.objects.all()

        context = {}
        list_admit=[]
        list_admit_id=[]
        for j in y:
            if j.name==s.name:
                context['name']=j.name
                list_admit.append(j.admit_date)
                list_admit_id.append(j.id)
        list_admit.sort(reverse=True)
        list_admit_id.sort(reverse=True)

        context['app']=list_admit[0]
        context['id']=list_admit_id[0]
        for j in y:
            if j.name==s.name and j.admit_date==list_admit[0] and j.id==list_admit_id[0]:
                for u in room:
                    if u.room_type == j.room_type:
                        context['rent']=u.room_charge
                        context['room']=u.room_type
                        break
        dis_date=[]
        for l in k:
            if l.name==s.name:
                dis_date.append(l.date)
        dis_date.sort(reverse=True)
        context['dis']=dis_date[0]
        context['diff']=dis_date[0]-j.admit_date
        context['trent']=u.room_charge*int((dis_date[0]-j.admit_date).days)
        context['send']=False
        context['sen']=True
        currency = 'INR'
        amount = u.room_charge*int((dis_date[0]-j.admit_date).days)
        amount = amount*100
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
	    											currency=currency,
	    											payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        for key, value in context.items():
            listf[key] = value
        return render(request,'bill.html',context=context)
    return render(request,'discharge.html')