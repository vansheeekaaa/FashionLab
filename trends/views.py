from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Design, Vote, Avatar
from .forms import DesignForm

# View to display all designs
def index(request):
    designs = Design.objects.all()
    return render(request, 'index.html', {'designs': designs})

# View to submit a new design
def submit_design(request):
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.creator = request.user
            design.save()
            return redirect('index')
    else:
        form = DesignForm()
    return render(request, 'submit_design.html', {'form': form})

# View to vote on a design
#@login_required
def vote(request, design_id):
    try:
        design = Design.objects.get(pk=design_id)
    except Design.DoesNotExist:
        return HttpResponseBadRequest("Design does not exist")
    
    if request.method == 'POST':
        Vote.objects.create(voter=request.user, design=design)
        return redirect('index')
    return render(request, 'vote.html', {'design': design})

# View for the lab page
def lab(request):
    return render(request, 'lab.html')

# View for the win page
def win(request):
    return render(request, 'win.html')

# View to create and customize an avatar
def create(request):
    return render(request, 'create.html')

#@login_required
def create_avatar(request):
    if request.method == 'POST':
        avatar_url = request.POST.get('avatar_url')
        if avatar_url:
            Avatar.objects.create(user=request.user, url=avatar_url)
            return redirect('index')
        return HttpResponseBadRequest("Avatar URL not found")
    return render(request, 'create_avatar.html')







def my_closet(request):
    return render(request, 'my_closet.html')
