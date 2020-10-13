from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.


def login_view(request):
	form = AuthenticationForm(request, data=request.POST or None)
	if form.is_valid():
		user_ = form.get_user()
		login(request, user_)
		return redirect("/")
	return render(
		request,
		"accounts/auth.html",
		{"form": form, "btn_label": "Login", "title": "Login Page"},
	)


def logout_view(request):
	if request.method == "POST":
		logout(request)
		return redirect("/login")
	return render(
		request, 
		"accounts/auth.html",
		{"form": None, "btn_label": "Logout", "title": "Logout Page", "description": "Are you sure you want to log out?"}
	)


def registration_view(request):
	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		user.set_password(form.cleaned_data.get("password1"))
		user.save()
		print(form.cleaned_data)
		login(request, user)
		return redirect("/")
	return render(
		request, 
		"accounts/auth.html", 
		{"form": form, "btn_label": "Register", "title": "Registration Page"}
	)
