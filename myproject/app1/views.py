import os,time
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *

def welcome(request):
	return render(request, 'Welcome.html')

#Login
def login(request):
	if request.method=='POST':
		e1=request.POST['T1']
		passwd=request.POST['T2']
		try:
			obj=logindata.objects.get(email=e1, password=passwd)
			usertype=obj.usertype

			request.session['usertype']=usertype
			request.session['email']=e1
			if usertype=='admin':
				return HttpResponseRedirect('/admin_home/')
			elif usertype=='student':
				return HttpResponseRedirect('/student_home/')
			elif usertype=='employee':
				return HttpResponseRedirect('/employee_home')
		except:

			msg="Wrong E-mail or Password"
			return render(request, 'Login.html', {'msg':msg})
	else:
		return render(request, 'Login.html')

#Logout
def logout(request):
	try:
		del request.session['email']
		del request.session['usertype']
	except:
		pass
	return HttpResponseRedirect('/login/')

#Authorisation Error
def auth_error(request):
	return render(request, 'AuthError.html')

#Homes
def home(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		if ut=='admin':
			return HttpResponseRedirect('/admin_home/')
		elif ut=='employee':
			return HttpResponseRedirect('/employee_home/')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def admin_home(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		if ut=='admin':
			return render(request, 'AdminHome.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def employee_home(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		if ut=='employee':
			return render(request, 'EmployeeHome.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def student_home(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='student':
			obj=student.objects.get(email=e1)
			return render(request, 'StudentHome.html', {'data':obj})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Data(Show list in tabular form)
def student_data(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']

		if ut=='admin' or ut=='employee':
			obj=student.objects.all()
			pho=photodata.objects.all()
			fee=installment.objects.all()
			return render(request,'ShowStudent.html', {'data':obj, 'pic' : pho, 'dat': fee})
		else:
			return HttpResponseRedirect('/auth_error')
	else:
		return HttpResponseRedirect('/auth_error')

def employee_data(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin':
			obj=employee.objects.all()
			return render(request,'ShowEmployee.html', {'data':obj})
		else:
			HttpResponseRedirect('/auth_error/')
	else:
		HttpResponseRedirect('/auth_error/')

#New Registration
def student_reg(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		if ut=='admin' or ut=='employee':
			if request.method == 'POST':
				st = student()
				log = logindata()

				name = request.POST['T1']
				class_stud = request.POST['T2']
				roll = request.POST['T3']
				email = request.POST['T4']
				passwd=request.POST['T5']
				#Get Photo
				upload_file = request.FILES['F1']
				path = os.path.basename(upload_file.name)

				file_ext = os.path.splitext(path)[1][1:]
				filename = str(int(time.time())) + '.' + file_ext
				fs = FileSystemStorage()
				fs.save(filename, upload_file)
				# Adding Photo to photodata Table
				obj = photodata()
				obj.email = email
				obj.photo = filename
				obj.save()
				# Saving student data
				st.name = name
				st.class_stud = class_stud
				st.rollno = roll
				st.email = email
				st.photo=filename
				st.save()
				#Saving login data
				log.email = email
				log.password=passwd
				log.usertype = 'student'
				log.save()

				return render(request, 'StudentRegistration.html', {'msg': 'Data Saved'})
			else:
				return render(request, 'StudentRegistration.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def employee_reg(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']

		if ut == 'admin':
			if request.method == 'POST':
				em = employee()
				log = logindata()

				name = request.POST['T1']
				id = request.POST['T2']
				contact = request.POST['T3']
				email = request.POST['T4']
				passwd = request.POST['T5']
				# Get Photo
				upload_file = request.FILES['F1']
				path = os.path.basename(upload_file.name)

				file_ext = os.path.splitext(path)[1][1:]
				filename = str(int(time.time())) + '.' + file_ext
				fs = FileSystemStorage()
				fs.save(filename, upload_file)
				# Adding Photo to photodata Table
				obj = photodata()
				obj.email = email
				obj.photo = filename
				obj.save()
				#Saving employee data
				em.name = name
				em.id = id
				em.contact = contact
				em.email = email
				em.photo=filename
				em.save()
				#Adding logindata to logindata table
				log.email = email
				log.password = passwd
				log.usertype = 'employee'
				log.save()

				return render(request, 'EmployeeRegistration.html', {'msg': 'Data Saved'})
			else:
				return render(request, 'EmployeeRegistration.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Search Student/Employee
def search_student(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin' or ut=='employee':
			if request.method=='POST':
				e2=request.POST['E1']
				obj = student.objects.get(email=e2)
				pic = photodata.objects.filter(email=e2)
				return render(request, 'SearchStudent.html', {'data': obj, 'data1': pic, 'email': e1})
			else:
				return render(request, 'SearchStudent.html', {'result': 'Enter a valid E-mail'})
		else:
			HttpResponseRedirect('/auth_error')
	else:
		HttpResponseRedirect('/auth_error')

def search_student0(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin' or ut=='employee':
			if request.method=='POST':
				e2=request.POST['E1']
				obj = student.objects.get(email=e2)
				pic = photodata.objects.filter(email=e2)
				obj.employee_email=e1
				obj.save()
				return render(request, 'SearchStudent.html', {'data': obj, 'data1': pic, 'email': e1})
			else:
				return render(request, 'SearchStudent0.html', {'result': 'Enter a valid E-mail'})
		else:
			HttpResponseRedirect('/auth_error')
	else:
		HttpResponseRedirect('/auth_error')

def search_employee(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin':
			if request.method=='POST':
				e2=request.POST['E1']
				obj = employee.objects.filter(email=e2)
				pic = photodata.objects.filter(email=e2)
				return render(request, 'SearchEmployee.html', {'data': obj, 'data1': pic})
			else:
				return render(request, 'SearchEmployee.html', {'result': 'Enter a valid E-mail'})
		else:
			HttpResponseRedirect('/auth_error')
	else:
		HttpResponseRedirect('/auth_error')

def search_employee0(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin':
			if request.method=='POST':
				e2=request.POST['E1']
				obj = employee.objects.get(email=e2)
				pic = photodata.objects.filter(email=e2)
				return render(request, 'SearchEmployee.html', {'data': obj, 'data1': pic, 'email': e1})
			else:
				return render(request, 'SearchEmployee0.html')
		else:
			HttpResponseRedirect('/auth_error')
	else:
		HttpResponseRedirect('/auth_error')

#Edit Employee
def edit_employee0(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin':
				return render(request, 'EditEmployee0.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def edit_employee(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin':
			if request.method == 'POST':
				email = request.POST['H1']
				obj = employee.objects.get(email=email)
				return render(request, 'EditEmployee.html', {'data': obj})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def save_employee(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin' or ut == 'employee':
			if request.method == 'POST':

				name = request.POST['T1']
				id = request.POST['T2']
				contact = request.POST['T3']
				email=request.POST['T4']

				obj = employee.objects.get(email=email)
				obj.name = name
				obj.id = id
				obj.contact = contact
				obj.email=email
				obj.save()
				return render(request, 'EditStudent1.html', {'msg': 'Changes Saved'})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Edit Student
def edit_student0(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin' or ut == 'employee':
				return render(request, 'EditStudent0.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def edit_student(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin' or ut == 'employee':
			if request.method == 'POST':
				email = request.POST['H1']
				obj = student.objects.get(email=email)
				return render(request, 'EditStudent.html', {'data': obj})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def save_student(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		e1=request.session['email']
		if ut == 'admin' or ut == 'employee':
			if request.method == 'POST':
				name = request.POST['T1']
				class_stud = request.POST['T2']
				rollno = request.POST['T3']
				email=request.POST['T4']
				fees=request.POST['T5']
				fees_dep = request.POST['T6']
				obj = student.objects.get(email=email)
				obj.name = name
				obj.class_stud = class_stud
				obj.rollno=rollno
				obj.fees=fees
				obj.fees_dep=fees_dep
				obj.employee_email=e1
				obj.save()
				return render(request, 'EditStudent1.html', {'msg': 'Changes Saved' ,'data': obj} )
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Delete Student
def delete_student0(request):

	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin' or ut == 'employee':
				return render(request, 'DeleteStudent0.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def delete_student(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin' or ut == 'employee':
			if request.method == 'POST':
				email = request.POST["H1"]
				obj = student.objects.get(email=email)
				log = logindata.objects.get(email=email)
				obj.delete()
				log.delete()
				return render(request, 'DeleteStudent.html', {'msg': 'Data Deleted Successfully'})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Delete Employee
def delete_employee0(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin':
				return render(request, 'DeleteEmployee0.html')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def delete_employee(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		if ut == 'admin':
			if request.method == 'POST':
				email = request.POST["H1"]
				obj = employee.objects.get(email=email)

				log = logindata.objects.get(email=email)
				obj.delete()
				log.delete()
				return render(request, 'DeleteEmployee.html', {'msg': 'Data Deleted Successfully'})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Profiles
def profile(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		if ut=='admin':
			return HttpResponseRedirect('/admin_profile/')
		elif ut=='employee':
			return HttpResponseRedirect('/employee_profile')
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def student_profile(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin' or ut=='employee':
			if request.method=='POST':
				e2=request.POST['T1']
				obj=student.objects.filter(email=e2)
				obj1=photodata.objects.filter(email=e2)
				return render(request, 'StudentProfile.html', {'data':obj, 'email':e2,'pic':obj1})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def employee_profile(request):
	if request.session.has_key('usertype'):

		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='employee':
			obj=employee.objects.filter(email=e1)
			obj1=photodata.objects.filter(email=e1)
			return render(request, 'EmployeeProfile.html', {'data':obj, 'email':e1,'pic':obj1})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

def admin_profile(request):
	if request.session.has_key('usertype'):
		ut=request.session['usertype']
		e1=request.session['email']
		if ut=='admin':
			obj=admindata.objects.filter(email=e1)
			obj1=photodata.objects.filter(email=e1)
			return render(request, 'AdminProfile.html', {'data':obj, 'email':e1,'pic':obj1})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Upload Photo
def uploadphoto(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		e1 = request.session['email']
		if ut == 'employee' or ut=='admin':
			if request.method == 'POST':
				e2=request.POST['T1']
				upload_file = request.FILES['F1']
				path = os.path.basename(upload_file.name)

				file_ext = os.path.splitext(path)[1][1:]
				filename = str(int(time.time())) + '.' + file_ext
				fs = FileSystemStorage()
				fs.save(filename, upload_file)
				# Adding Photo to photodata Table
				obj=photodata()
				obj.email = e2
				obj.photo = filename
				obj.save()
				# Adding Photo to student Table
				st=student.objects.get(email=e2)
				st.photo=filename
				st.save()
				return render(request, 'UploadPhoto.html', {'msg':'Photo Uploaded Successfully'})
			else:
				return render(request,'UploadPhoto.html')
		else:
			return render(request, 'AuthError.html')

	else:
		return render(request, 'AuthError.html')

def uploadphotoadmin(request):
	if request.session.has_key('usertype'):
		usertype = request.session['usertype']
		e1 = request.session['email']
		if usertype == 'admin':
			if request.method == 'POST':
				upload_file = request.FILES['F1']
				path = os.path.basename(upload_file.name)

				file_ext = os.path.splitext(path)[1][1:]
				filename = str(int(time.time())) + '.' + file_ext
				fs = FileSystemStorage()
				fs.save(filename, upload_file)

				obj=photodata()
				obj.email = e1
				obj.photo = filename
				obj.save()
				return render(request, 'UploadPhotoAdmin.html', {'msg': 'Photo Uploaded Successfully'})
			else:
				return render(request, 'UploadPhotoAdmin0.html')

		else:
			return render(request, 'AuthError.html')

	else:
		return render(request, 'AuthError.html')

def uploadphotoemployee(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		e1 = request.session['email']
		if ut == 'employee' or ut=='admin':
			if request.method == 'POST':
				e2=request.POST['T1']
				upload_file = request.FILES['F1']
				path = os.path.basename(upload_file.name)

				file_ext = os.path.splitext(path)[1][1:]
				filename = str(int(time.time())) + '.' + file_ext
				fs = FileSystemStorage()
				fs.save(filename, upload_file)
				# Adding Photo to photodata Table
				obj=photodata()
				obj.email = e2
				obj.photo = filename
				obj.save()
				# Adding Photo to employee Table
				em=employee.objects.get(email=e2)
				em.photo=filename
				em.save()
				return render(request, 'UploadPhotoEmployee.html', {'msg':'Photo Uploaded Successfully'})
			else:
				return render(request,'UploadPhotoEmployee.html')
		else:
			return render(request, 'AuthError.html')

	else:
		return render(request, 'AuthError.html')

#Save Fees

def save_student_fees(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		e1=request.session['email']
		if ut == 'admin' or ut == 'employee':
			if request.method == 'POST':
				email=request.POST['T4']
				fees_dep = request.POST['T6']
				obj = student.objects.get(email=email)
				fee=obj.fees
				obj.employee_email = e1
				obj.fees_dep=fees_dep

				obj.save()
				foo=feesrecord()
				foo.depositby=e1
				dep=fee-fees_dep
				foo.amount=dep
				foo.save()
				return render(request, 'EditStudent1.html', {'msg': 'Changes Saved'})
		else:
			return HttpResponseRedirect('/auth_error/')
	else:
		return HttpResponseRedirect('/auth_error/')

#Change Password
def change_password_admin(request):
	if request.session.has_key('usertype'):
		usertype = request.session['usertype']
		e1 = request.session['email']
		if usertype == 'admin':
			if request.method == 'POST':
				curpass=request.POST['H2']
				newpass=request.POST['H3']
				obj=logindata.objects.get(email=e1)
				curpass1=obj.password
				if curpass==curpass1:
					obj.password = newpass
					obj.save()
					return render(request, 'ChangePasswordAdmin.html', {'msg': 'Password Changed Successfully'})
				else:
					return render(request,'ChangePasswordAdmin.html', {'msg':'Wrong Current Password'})
			else:
				return render(request,'ChangePasswordAdmin.html')
		else:
			return render(request, 'AuthError.html')

	else:
		return render(request, 'AuthError.html')

def change_password_employee(request):
	if request.session.has_key('usertype'):
		usertype = request.session['usertype']
		e1 = request.session['email']
		if usertype == 'admin' or usertype=='employee':
			if request.method == 'POST':
				curpass=request.POST['H2']
				newpass=request.POST['H3']

				obj=logindata.objects.get(email=e1)
				curpass1=obj.password
				if curpass==curpass1:
					obj.password = newpass
					obj.save()
					return render(request, 'ChangePasswordEmployee.html', {'msg': 'Password Changed Successfully'})
				else:
					return render(request,'ChangePasswordEmployee.html', {'msg':'Wrong Current Password'})
			else:
				return render(request,'ChangePasswordEmployee.html')
		else:
			return render(request, 'AuthError.html')

	else:
		return render(request, 'AuthError.html')

def installments(request):
	obj=installment.objects.all()
	return render(request, 'install.html', {'data':obj})

def install_data(request):
	if request.session.has_key('usertype'):
		ut = request.session['usertype']
		e1 = request.session['email']
		if ut=='employee':
			if request.method=='POST':
				obj=installment()
				email=request.POST['sid']
				fees=request.POST['fee']
				obj.sid=email
				obj.amount=fees
				obj.depositedby=e1
				obj.save()
				return HttpResponseRedirect('/employee_home/')
			else:
				return render(request,'addInstallment.html',{'msg':'ENTER DATA'})
		else:
			return render(request, 'AuthError.html')
	else:
		return render(request, 'AuthError.html')