from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator

from allauth.account.views import SignupView

class RegView(SignupView):
    form_class = MyUserCreationForm
    template_name = 'account/register.html'

class RegisterView(View):
    def get(self,request):
        form = MyUserCreationForm()
        return render(request,'account/register.html',{'form':form})
    
    def post(self,request):
        print("inside post")
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            print("inside form valid")
            form.save()
            messages.add_message(request, messages.INFO, "User created successfully")
            return HttpResponseRedirect(reverse('account:login'))
        return render(request,'account/register.html',{'form':form})
            
class LoginView(View):
    def get(self,request):
        return HttpResponse("hello")
    

