from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'celebritypicker/home.html')

def signup (request):
    return render(request, '/signup.html')
