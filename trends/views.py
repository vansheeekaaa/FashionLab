from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import DesignForm
from .models import DesignSubmission, Upvote, ClosetItem# Ensure Upvote model is imported
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User

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
            
            # Determine where to redirect based on the referrer
            referrer = request.META.get('HTTP_REFERER', '')
            if 'create' in referrer:
                return redirect('create')
            else:
                return redirect('lab')
        else:
            return render(request, 'lab.html', {'error': 'Invalid email or password', 'show_login': True})

    return render(request, 'lab.html', {'show_login': True})

from django.urls import reverse

def signup(request):
    next_page = request.GET.get('next', 'lab')  # Default to 'lab' if no 'next' parameter is provided
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            error = 'Email is already registered'
            return render(request, 'signup.html', {'error': error})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name  # Save the name in the user's first_name field
        user.save()
        auth_login(request, user)

        if next_page == 'create':
            return redirect('create')
        else:
            return redirect('lab')

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('lab')

def submit_design(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        design_link = request.POST.get('design_link')

        design_submission = DesignSubmission(
            name=name,
            email=email,
            design_link=design_link,
            user=request.user 
        )
        design_submission.save()
        return redirect('success')  

    context = {
        'user_name': request.user.get_full_name() if request.user.get_full_name() else request.user.username,
        'user_email': request.user.email
    }
    return render(request, 'submit_design.html', context)

def index(request):
    return render(request, 'index.html')

def lab(request):
    user_authenticated = request.user.is_authenticated
    return render(request, 'lab.html', {'user_authenticated': user_authenticated})

def win(request):
    return render(request, 'win.html')

def create(request):
    user_authenticated = request.user.is_authenticated
    if request.method == 'POST':
        if user_authenticated:
            return redirect('submit_design')
        else:
            return redirect('signup')

    return render(request, 'create.html', {'user_authenticated': user_authenticated})

def my_closet(request):
    user = request.user
    closet_items = ClosetItem.objects.filter(user=user)
    designs = [item.design for item in closet_items]
    return render(request, 'my_closet.html', {'designs': designs})

def success(request):
    return render(request, 'success.html')

def vote_view(request):
    designs = DesignSubmission.objects.all()
    return render(request, 'vote.html', {'designs': designs})

def upvote_design(request, design_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        design = get_object_or_404(DesignSubmission, pk=design_id)
        user = request.user

        # Check if the user has already upvoted this design
        upvote, created = Upvote.objects.get_or_create(user=user, design=design)

        if not created:
            # User already upvoted this design, so remove the upvote
            upvote.delete()
            design.votes -= 1
            upvoted = False
        else:
            # New upvote
            design.votes += 1
            upvoted = True

        design.save()
        return JsonResponse({'votes': design.votes, 'upvoted': upvoted})

    return JsonResponse({'error': 'POST request required'}, status=405)

def add_to_closet(request, design_id):
    if request.method == 'POST':
        try:
            design = DesignSubmission.objects.get(id=design_id)
            if design:
                if not ClosetItem.objects.filter(user=request.user, design=design).exists():
                    ClosetItem.objects.create(user=request.user, design=design)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Design already in closet'})
        except DesignSubmission.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Design does not exist'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def lab(request):
    designs = DesignSubmission.objects.all()
    user_upvoted_designs = []

    if request.user.is_authenticated:
        user_upvoted_designs = Upvote.objects.filter(user=request.user).values_list('design_id', flat=True)

    return render(request, 'lab.html', {
        'designs': designs,
        'user_upvoted_designs': user_upvoted_designs,
        'user_authenticated': request.user.is_authenticated
    })

def remove_from_closet(request, design_id):
    if request.method == 'POST':
        try:
            design = get_object_or_404(DesignSubmission, id=design_id)
            closet_item = ClosetItem.objects.filter(user=request.user, design=design)
            if closet_item.exists():
                closet_item.delete()
                return JsonResponse({'success': True})
        except DesignSubmission.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Design does not exist'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})