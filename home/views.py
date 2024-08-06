from django.shortcuts import render

# Create your views here.
def LoadHome(request):
    return render(request, 'Home.html')

def LoadManual(request):
    return render(request, 'Manual.html')

def LoadUser(request):
    return render(request, 'User.html')

def LoadRepo(request):
    return render(request, 'Repo.html')

def LoadOrg(request):
    return render(request, 'Org.html')