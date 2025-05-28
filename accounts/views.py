from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') # Or a homepage if you have one, e.g., redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    # success_url = reverse_lazy('home') # Define a 'home' url or redirect to '/' or another page

# Logout view can be used directly from django.contrib.auth.views in urls.py
# or you can define a simple wrapper if needed for more context/logic later.
