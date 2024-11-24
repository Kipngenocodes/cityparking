from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

def home(request):
    # Checking if they are logging in.
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST.get("role")  # Capture the role from the dropdown
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)

            # Handle role-based redirection
            if role == "admin" and user.is_superuser:
                messages.success(request, "Welcome Admin! Enjoy full access.")
                return redirect('admin_dashboard')  # Admin-specific dashboard
            elif role == "regular" and not user.is_superuser:
                messages.success(request, "Welcome Regular User! Enjoy your services.")
                return redirect('regular_dashboard')  # Regular user dashboard
            elif role == "guest":
                messages.success(request, "Welcome Guest! Enjoy limited access.")
                return redirect('guest_dashboard')  # Guest dashboard
            else:
                # If role doesn't match user type
                messages.error(request, "Invalid role selected for this account.")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

# Registration view
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save to the database yet
            role = form.cleaned_data['role']

            # Assign Admin privileges if role is 'admin'
            if role == 'admin':
                user.is_staff = True  # Grant staff status
                user.is_superuser = True  # Grant superuser privileges
            
            user.save()  # Save to the database
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

# Logout functionality
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# Role-specific dashboards
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {})

@login_required
def regular_dashboard(request):
    return render(request, 'regular_dashboard.html', {})

@login_required
def guest_dashboard(request):
    return render(request, 'guest_dashboard.html', {})
