from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


def login_user(request):
    return render(
        request,
        "users/login.html",
    )


class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(to="website:index")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Account for {username} created successfully")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})
