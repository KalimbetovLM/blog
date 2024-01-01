from django.shortcuts import render,redirect
from django.views import View
from users.forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

class RegisterView(View):

    def get(self,request):
        form = RegisterForm()
        context = {
            'form':form
        }
        return render(request,'users/register.html',context)
    
    def post(self,request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            context = {
                'form':form
            }
            return render(request,'users/register.html',context)


class LoginView(View):

    def get(self,request):
        form = LoginForm()
        context = {
            'form':form
        }
        return render(request,'users/login.html',context)
    
    def post(self,request):
        form = AuthenticationForm(data=request.POST)
        user = form.get_user()
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                return redirect("posts:post_list")    
            else:
                return HttpResponse("Please,enter correct password or username")
        else:
            return render(request,'users/login.html',{"form":form})

class LogOutView(View):

    def get(self,request):
        logout(request)
        messages.info(request,"You have successfully logged out")
        return redirect("posts:post_list")
        