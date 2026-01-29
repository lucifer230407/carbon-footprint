from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, SignupForm
from .models import LoginHistory


def signup(request):
    """Handle user registration with custom form"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                # Create new user
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password']
                )
                
                # Log signup activity
                LoginHistory.objects.create(
                    user=user,
                    login_type='signup'
                )
                
                # Automatically log the user in after signup
                login(request, user)
                messages.success(request, f'Welcome {user.first_name or user.username}! Your account has been created successfully.')
                return redirect('dashboard')
            
            except Exception as e:
                messages.error(request, f'An error occurred during signup: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    """Handle user login with custom form"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Log login activity
                LoginHistory.objects.create(
                    user=user,
                    login_type='login'
                )
                
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect to next page if provided, otherwise to dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def login_history(request):
    """Display user's login history"""
    user_login_history = LoginHistory.objects.filter(user=request.user)
    
    return render(request, 'login_history.html', {
        'login_history': user_login_history
    })

