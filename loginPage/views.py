from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from . import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout


class LoginView(View):
    form_class = forms.LoginForm
    template_name = 'loginPage/login.html'
    form = form_class(None)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:homepage')
        else:
            return render(request,
                          self.template_name,
                          {'form': self.form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:homepage')
        msg = "Invalid Login Credentials"
        return render(request,
                      self.template_name,
                      {'form': self.form,
                       'msg': msg})


def logoutview(request):
    logout(request)
    return redirect('login_App:index')
