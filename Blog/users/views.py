from django.shortcuts import render
<<<<<<< HEAD
# Create your views here.
=======
<<<<<<< HEAD
# Create your views here.
=======
>>>>>>> feea372ff8d2b558b178edc6f857898fb38b1e6f
>>>>>>> aecf3b8f20cf3b4e6b08ba79e5e6ac054ba1aace
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> aecf3b8f20cf3b4e6b08ba79e5e6ac054ba1aace
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blogapp:index'))

def register(request):
    #Register a new user.
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
            password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('blogapp:index'))
    
    context = {'form': form}
<<<<<<< HEAD
    return render(request, 'users/register.html', context)
=======
    return render(request, 'users/register.html', context)
=======
# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    if request.method!='POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #login user and redirect to home page
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
        
    context={'form':form}
    return render(request,'users/register.html',context)
>>>>>>> feea372ff8d2b558b178edc6f857898fb38b1e6f
>>>>>>> aecf3b8f20cf3b4e6b08ba79e5e6ac054ba1aace
