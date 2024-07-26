from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import DesignForm
from .models import DesignSubmission
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

def profile(request):
    return render(request, 'profile.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'lab.html', {'error': 'Invalid email or password', 'show_login': True})

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            auth_login(request, user) 
            return redirect('lab')
        else:
            return render(request, 'lab.html', {'error': 'Invalid email or password', 'show_login': True})
    
    return render(request, 'lab.html', {'show_login': True})

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            error = 'Email is already registered'
            return render(request, 'signup.html', {'error': error})

        user = User.objects.create_user(username=email, email=email, password=password)
        auth_login(request, user)
        return render(request, 'signup.html', {'success': 'Successfully signed up!'})
    
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('lab')

def submit_design(request):
    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DesignForm()
    return render(request, 'submit_design.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def lab(request):
    user_authenticated = request.user.is_authenticated
    return render(request, 'lab.html', {'user_authenticated': user_authenticated})

def win(request):
    return render(request, 'win.html')

def create(request):
    return render(request, 'create.html')

def my_closet(request):
    return render(request, 'my_closet.html')

def success(request):
    return render(request, 'success.html')

def vote_view(request):
    designs = DesignSubmission.objects.all()
    return render(request, 'vote.html', {'designs': designs})

def upvote_design(request, design_id):
    if request.method == 'POST':
        design = get_object_or_404(DesignSubmission, pk=design_id)
        design.votes += 1
        design.save()
        return JsonResponse({'votes': design.votes})
    return JsonResponse({'error': 'POST request required'})
