import sys
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .src.fetch import fetch1
from .src.analysis import analysis1

def Home(request):
    return render(request, 'repo_index.html')

# Create your views here.
async def GetRepoData(request):
    try: 
        data = await analysis1.GetRepoContributors('RavenTheshadow', 'BTL_LTNC')
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)


# Get Commit from repo
async def GetRepoData2(request):
    try: 
        data = await analysis1.GetRepoCommits('RavenTheshadow', 'BTL_LTNC')
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)


# Get Issues from repo
async def GetRepoData3(request):
    try: 
        data = await analysis1.GetRepoIssues('krahets', 'hello-algo')
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)
    
# Get Pull request from repo
async def GetRepoData4(request):
    try: 
        data = await analysis1.GetRepoPulls('krahets', 'hello-algo')
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)
    
