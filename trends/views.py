from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import DesignForm
from .models import DesignSubmission

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
    return render(request, 'lab.html')

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
