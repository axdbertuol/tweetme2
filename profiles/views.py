from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ProfileForm, UserProfileForm
from .models import Profile

# Create your views here.

def profile_update_view(request):
	if not request.user.is_authenticated:
		return redirect("/login?next=/profile/update")
	my_profile = request.user.profile
	user_data = {
		"first_name": request.user.first_name,
		"last_name": request.user.last_name,
		"email": request.user.email,
		"bio": my_profile.bio,
		"location": my_profile.location
	}
	profile_data = {
		"bio": my_profile.bio,
		"location": my_profile.location
	}
	# form = ProfileForm(request.POST or None, instance=my_profile, initial=user_data)
	user_form = UserProfileForm(request.POST or None, instance=request.user, initial=user_data)
	profile_form = ProfileForm(request.POST or None, instance=my_profile, initial=profile_data)
	if user_form.is_valid() and profile_form.is_valid():
		profile_obj = profile_form.save(commit=False)
		request.user.first_name = user_form.cleaned_data["first_name"]
		request.user.last_name = user_form.cleaned_data["last_name"]
		request.user.email = user_form.cleaned_data["email"]
		request.user.save()
		profile_obj.save()
	
	return render(
		request, 
		"profiles/form.html", 
		{"form": user_form, "btn_label": 'Save', 'title': 'Update Profile'}
	)
def profile_detail_view(request, username):
	#get the profile for the passed username
	qs = Profile.objects.filter(user__username=username)

	if not qs.exists():
		raise Http404
	profile_obj = qs.first()
	return render(
		request, 
		"profiles/detail.html", 
		{"username": username, "profile": profile_obj}
	)