from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import DesignForm

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

def success(request):
    return render(request, 'success.html')
