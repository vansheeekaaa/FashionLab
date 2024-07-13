from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import DesignForm
from django.views.decorators.http import require_POST
from .models import DesignSubmission

def submit_design(request):
    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success')  # Redirect to a success page after processing
    else:
        form = DesignForm()
    return render(request, 'submit_design.html', {'form': form})

# View to display all designs
def index(request):
    return render(request, 'index.html')

# View for the lab page
def lab(request):
    return render(request, 'lab.html')

# View for the win page
def win(request):
    return render(request, 'win.html')
 
# View to create and customize an avatar
def create(request):
    return render(request, 'create.html')

def my_closet(request):
    return render(request, 'my_closet.html')
    analyze_user_preferences(user)

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
    # Handle GET request if needed
    return JsonResponse({'error': 'POST request required'})

def vote(request, design_id):
    design = get_object_or_404(DesignSubmission, pk=design_id)
    if request.method == 'POST':
        Vote.objects.create(voter=request.user, design=design)
        design.votes += 1
        design.save()
        return redirect('vote_success', design_id=design.id)
    return render(request, 'vote.html', {'design': design})

def vote_success(request, design_id):
    design = get_object_or_404(DesignSubmission, pk=design_id)
    return render(request, 'vote.html', {'design': design, 'success': True})
