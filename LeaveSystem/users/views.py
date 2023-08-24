from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserAddForm,UserLogin
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from employee.models import *

# Create your views here.

#register user
def register(request):
    if request.method=='POST':
        form=UserAddForm(request.POST)#render form
        if form.is_valid():#check if form is valid
            instance=form.save(commit=False)
            instance.save()
            username=form.cleaned_data.get("username")

            messages.success(request,'Account created for {0} !!!'.format(username))
            return redirect('users:login')
        else:
            messages.error(request,'Username or password invalid')
            return redirect('users:register')

    #for get requests
    form=UserAddForm()
    context={
          'form':form,
          'title':'Register Users'
    }
    return render(request,'users/register.html',context)

def login_view(request):
    login_user=request.user
    if request.method=='POST':
        form=UserLogin(data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)
            if user and user.is_active:
                login(request,user)
                if login_user.is_authenticated:
                    return redirect('dashboard:dashboard')
                else:
                    messages.error(request,"Invalid Account")
                    return redirect('users:login')
            else:
                return HttpResponse('Not registered.Consult your manager')
            
    dataset=dict()
    form=UserLogin()

    dataset['form']=form
    return render(request,'users/login.html',dataset)
        

def logout_view(request):
	logout(request)
	return redirect('users:login')


def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request,user)

			messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('users:change_password')
		else:
			messages.error(request,'Error,changing password',extra_tags = 'alert alert-warning alert-dismissible show' )
			return redirect('users:change_password')
			
	form = PasswordChangeForm(request.user)
	return render(request,'users/change_password_form.html',{'form':form})


def users_list(request):
	employees = Employee.objects.all()
	return render(request,'users/users_table.html',{'employees':employees,'title':'Users List'})

def users_unblock(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = False
	emp.save()
	user.is_active = True
	user.save()

	return redirect('users:users')


def users_block(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = True
	emp.save()
	
	user.is_active = False
	user.save()
	
	return redirect('users:users')



def users_blocked_list(request):
	blocked_employees = Employee.objects.all_blocked_employees()
	return render(request,'users/all_deleted_users.html',{'employees':blocked_employees,'title':'blocked users list'})

# def user_profile_view(request):
# 	'''
# 	user profile view -> staffs (No edit) only admin/HR can edit.
# 	'''
# 	user = request.user
# 	if user.is_authenticated:
# 		employee = Employee.objects.filter(user = user).first()
		

# 		dataset = dict()
# 		dataset['employee'] = employee
	
		

# 		return render(request,'dashboard/employee_detail.html',dataset)
# 	return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")
