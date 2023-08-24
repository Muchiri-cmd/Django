from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from employee.forms import EmployeeCreateForm
from leave.models import Leave
from employee.models import *
from leave.forms import LeaveCreationForm


#shows the main dashboard
def dashboard(request):
	
	'''
	Summary of all apps - display here with charts etc.
	eg.lEAVE - PENDING|APPROVED|RECENT|REJECTED - TOTAL THIS MONTH or NEXT MONTH
	EMPLOYEE - TOTAL | GENDER 
	CHART - AVERAGE EMPLOYEE AGES
	'''
	dataset = dict()
	user = request.user
	employees = Employee.objects.all()
	
	if not request.user.is_authenticated:
		return redirect('users:login')
	
	if request.user.is_superuser:
		#filter leaves for staff
		head_department_ids =Department.objects.values_list('department_head_id',flat = True)
		leaves = Leave.objects.filter(user_id__in = head_department_ids,status='pending').order_by('-created')
		staff_leaves = Leave.objects.filter(user = user)
		#Get department based on user type
		if request.user.is_superuser or request.user.is_staff:
			try:
				department=Department.objects.get(department_head_id=request.user.id)
			except Department.DoesNotExist:
				department=None

		else:
			department=None

		#filter employees based on department
		if department:
			employees = employees.filter(department = department)

		
		dataset['employees'] = employees
		dataset['leaves'] = leaves
		
		dataset['staff_leaves'] = staff_leaves
		dataset['title'] = 'summary'
	

		return render(request,'dashboard/dashboard_index.html',dataset)


	
	
	#Get depaartment of current user
	user_department_id = get_department_id_by_user_id(request.user.id)
	leaves = Leave.objects.filter(department_id = user_department_id,status = 'pending').order_by('-created')
	
	staff_leaves = Leave.objects.filter(user = user)
	#Get department based on user type
	if request.user.is_superuser or request.user.is_staff:
		try:
			department=Department.objects.get(department_head_id=request.user.id)
		except Department.DoesNotExist:
			department=None

	else:
		department=None

	#filter employees based on department
	if department:
		employees = employees.filter(department = department)

	
	dataset['employees'] = employees
	dataset['leaves'] = leaves
	
	dataset['staff_leaves'] = staff_leaves
	dataset['title'] = 'summary'
	

	return render(request,'dashboard/dashboard_index.html',dataset)



#dashboard page for employees app
def dashboard_employees(request):
	if not (request.user.is_authenticated and request.user.is_superuser or request.user.is_staff):
		return redirect('/')

	dataset = dict()
	departments = Department.objects.all()
	employees = Employee.objects.all()


	#Get department based on user type
	if request.user.is_superuser or request.user.is_staff:
		try:
			department=Department.objects.get(department_head_id=request.user.id)
		except Department.DoesNotExist:
			department=None

	else:
		department=request.user.employee.department

	#filter employees based on department
	if department:
		employees = employees.filter(department = department)

	#pagination(divide pages)
	query = request.GET.get('search')
	if query:
		employees = employees.filter(
			Q(firstname__icontains = query) |
			Q(lastname__icontains = query)
		)



	paginator = Paginator(employees, employees.count()) #show 10 employee lists per page

	page = request.GET.get('page')
	employees_paginated = paginator.get_page(page)



	blocked_employees = Employee.objects.all_blocked_employees()

	dataset['departments'] = departments
	dataset['employees_paginated'] = employees_paginated
	dataset['blocked_employees'] = blocked_employees

	print(departments,employees_paginated,)
	return render(request,'dashboard/employee_app.html',dataset)




def dashboard_employees_create(request):
	if not (request.user.is_authenticated and request.user.is_superuser or request.user.is_staff):
		return redirect('/')

	if request.method == 'POST':
		form = EmployeeCreateForm(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.POST.get('user')
			assigned_user = User.objects.get(id = user)

			instance.user = assigned_user

			instance.title = request.POST.get('title')
			instance.image = request.FILES.get('image')
			instance.firstname = request.POST.get('firstname')
			instance.lastname = request.POST.get('lastname')
			instance.othername = request.POST.get('othername')
			
			instance.birthday = request.POST.get('birthday')

			

			



			role = request.POST.get('role')
			role_instance = Role.objects.get(id = role)
			instance.role = role_instance

			instance.startdate = request.POST.get('startdate')
			instance.employeetype = request.POST.get('employeetype')
			instance.employeeid = request.POST.get('employeeid')
			instance.dateissued = request.POST.get('dateissued')

			

			instance.save()

			

			return  redirect('dashboard:employees')
		else:
			messages.error(request,'Trying to create dublicate employees with a single user account ',extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('dashboard:employeecreate')


	dataset = dict()
	form = EmployeeCreateForm()
	dataset['form'] = form
	dataset['title'] = 'register employee'
	return render(request,'dashboard/employee_create.html',dataset)


def employee_edit_data(request,id):
	if not (request.user.is_authenticated and request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	employee = get_object_or_404(Employee, id = id)
	if request.method == 'POST':
		form = EmployeeCreateForm(request.POST or None,request.FILES or None,instance = employee)
		if form.is_valid():
			instance = form.save(commit = False)

			user = request.POST.get('user')
			assigned_user = User.objects.get(id = user)

			instance.user = assigned_user

			instance.image = request.FILES.get('image')
			instance.firstname = request.POST.get('firstname')
			instance.lastname = request.POST.get('lastname')
			instance.othername = request.POST.get('othername')
			
			instance.birthday = request.POST.get('birthday')

	
			department_id = request.POST.get('department')
			department = Department.objects.get(id = department_id)
			instance.department = department


			instance.hometown = request.POST.get('hometown')
			instance.region = request.POST.get('region')
			instance.residence = request.POST.get('residence')
			instance.address = request.POST.get('address')
			instance.education = request.POST.get('education')
			instance.lastwork = request.POST.get('lastwork')
			instance.position = request.POST.get('position')
			instance.ssnitnumber = request.POST.get('ssnitnumber')
			instance.tinnumber = request.POST.get('tinnumber')

			role = request.POST.get('role')
			role_instance = Role.objects.get(id = role)
			instance.role = role_instance

			instance.startdate = request.POST.get('startdate')
			instance.employeetype = request.POST.get('employeetype')
			instance.employeeid = request.POST.get('employeeid')
			instance.dateissued = request.POST.get('dateissued')

			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

			instance.save()
			messages.success(request,'Account Updated Successfully !!!',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:employees')

		else:

			messages.error(request,'Error Updating account',extra_tags = 'alert alert-warning alert-dismissible show')
			return HttpResponse("Form data not valid")

	dataset = dict()
	form = EmployeeCreateForm(request.POST or None,request.FILES or None,instance = employee)
	dataset['form'] = form
	dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
	return render(request,'dashboard/employee_create.html',dataset)






def dashboard_employee_info(request,id):
	if not request.user.is_authenticated:
		return redirect('/')
	
	employee = get_object_or_404(Employee, id = id)
	
	
	dataset = dict()
	dataset['employee'] = employee
	dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
	return render(request,'dashboard/employee_detail.html',dataset)






# ---------------------LEAVE SECTION-------------------------------------------

#gets department id based on user id
def get_department_id_by_user_id(user_id):
    try:
        employee = Employee.objects.get(user_id=user_id)
        department_id = employee.department_id
        return department_id
    except Employee.DoesNotExist:
        return None  # Handle the case where no employee with the given user_id is found

#get department_head_id based on department_id
def get_department_head_id_by_department_id(department_id):
	try:
		department = Department.objects.get(id=department_id)
		department_head_id = department.department_head_id
		return department_head_id
	except Department.DoesNotExist:
		return None  # Handle the case where no department with the given department_id is found

def leave_creation(request):
	if not request.user.is_authenticated:
		return redirect('users:login')

	#we get the id of the department user belongs to
	user_department_id = get_department_id_by_user_id(request.user.id)

	#get the department head for that department
	#department_head_id = get_department_head_id_by_department_id(user_department_id)
	
	if request.method == 'POST':
		form = LeaveCreationForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.user
			instance.user = user

			if user_department_id is not None:
				instance.department_id = user_department_id

			instance.save()

			#get the department head for that user
			#department_head_id = Department.objects.get(department_head_id = user_department_id)


			# print(instance.defaultdays)
			messages.success(request,'Leave Request Sent,wait for Managers response',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:createleave')

		messages.error(request,'failed to Request a Leave,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
		return redirect('dashboard:createleave')


	dataset = dict()
	form = LeaveCreationForm()
	dataset['form'] = form
	dataset['title'] = 'Apply for Leave'
	return render(request,'dashboard/create_leave.html',dataset)
	


def leaves_list(request):
	if not (request.user.is_staff or request.user.is_superuser):
		return redirect('/')
	
	if request.user.is_superuser:
		#filter leaves for staff
		head_department_ids =Department.objects.values_list('department_head_id',flat = True)
		leaves = Leave.objects.filter(user_id__in = head_department_ids,status='pending').order_by('-created')
		return render(request,'dashboard/leaves_recent.html',{'leave_list':leaves,'title':'leaves list-pending'})
	
	#Get depaartment of current user
	user_department_id = get_department_id_by_user_id(request.user.id)
	head_department_ids =Department.objects.values_list('department_head_id',flat = True)
	leaves = Leave.objects.filter(department_id = user_department_id,status = 'pending').exclude(user_id__in = head_department_ids).order_by('-created')
	return render(request,'dashboard/leaves_recent.html',{'leave_list':leaves,'title':'leaves list - pending'})



def leaves_approved_list(request):
	if not (request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	
	if request.user.is_superuser:
		#filter leaves for staff
		head_department_ids =Department.objects.values_list('department_head_id',flat = True)
		leaves = Leave.objects.filter(user_id__in = head_department_ids).order_by('-created')
		return render(request,'dashboard/leaves_list.html',{'leave_list':leaves,'title':'leaves list'})
	
	#Get depaartment of current user
	user_department_id = get_department_id_by_user_id(request.user.id)

	leaves = Leave.objects.filter(department_id=user_department_id,status='approved').order_by('-created') #approved leaves -> calling model manager method
	return render(request,'dashboard/leaves_approved.html',{'leave_list':leaves,'title':'approved leave list'})



def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/')

	leave = get_object_or_404(Leave, id = id)
	#print(leave.user)
	employee = Employee.objects.filter(user = leave.user)
	#print(employee)
	return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(leave.user.username,leave.status)})





def approve_leave(request,id):
	if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_staff):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	user = leave.user
	employee = Employee.objects.filter(user = user)
	leave.approve_leave

	#messages.error(request,'Leave successfully approved for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:userleaveview', id = id)


def cancel_leaves_list(request):
	if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_staff):
		return redirect('/')
	
	#Get depaartment of current user
	user_department_id = get_department_id_by_user_id(request.user.id)
	leaves = Leave.objects.filter(department_id = user_department_id,status = 'cancelled').order_by('-created') #approved leaves -> calling model manager method
	return render(request,'dashboard/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel leave list'})



def unapprove_leave(request,id):
	if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.unapprove_leave
	return redirect('dashboard:leaveslist') #redirect to unapproved list




def cancel_leave(request,id):
	if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_staff):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.leaves_cancel

	messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request,id):
	if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_staff):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view



def leave_rejected_list(request):

	dataset = dict()
	
	#Get depaartment of current user
	user_department_id = get_department_id_by_user_id(request.user.id)
	leave = Leave.objects.filter(department_id = user_department_id,status = 'rejected').order_by('-created') #approved leaves -> calling model manager method

	dataset['leave_list_rejected'] = leave
	return render(request,'dashboard/rejected_leaves_list.html',dataset)



def reject_leave(request,id):
	dataset = dict()
	leave = get_object_or_404(Leave, id = id)
	leave.reject_leave
	messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:leavesrejected')

	# return HttpResponse(id)


def unreject_leave(request,id):
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')

	return redirect('dashboard:leavesrejected')



#  staffs leaves table user only
def view_my_leave_table(request):
	# work on the logics
	if request.user.is_authenticated:
		user = request.user
		leaves = Leave.objects.filter(user = user)
		employee = Employee.objects.filter(user = user).first()
		print(leaves)
		dataset = dict()
		dataset['leave_list'] = leaves
		dataset['employee'] = employee
		dataset['title'] = 'Leaves List'
	else:
		return redirect('accounts:login')
	return render(request,'dashboard/staff_leaves_table.html',dataset)



