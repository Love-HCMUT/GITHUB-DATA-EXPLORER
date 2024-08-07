import sys
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .src.analysis import repo_analysis as analysis
from .src.fetch import fetch1
from .src.analysis import analysis1

def Home(request):
    return render(request, 'repo_index.html')

# Create your views here.
async def GetRepoData(request, owner, repo):
    try: 
        data = await analysis1.GetRepoContributors(owner, repo)
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)


# Get Commit from repo
async def GetRepoData2(request, owner, repo):
    try: 
        data = await analysis1.GetRepoCommits(owner, repo)
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)


# Get Issues from repo
async def GetRepoData3(request, owner, repo):
    try: 
        data = await analysis1.GetRepoIssues(owner, repo)
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)
    
# Get Pull request from repo
async def GetRepoData4(request, owner, repo):
    try: 
        data = await analysis1.GetRepoPulls(owner, repo)
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)
    

# Create your views here.

async def repo_languages(request, owner, repo):
    try:
        data = await analysis.get_percent_languages(owner, repo)
        return JsonResponse(data)
    except Exception as e:
        return HttpResponse(status=404)
        
    
async def repo_info(request, owner = 'RavenTheShadow', repo = 'BTL_LTNC'):
    try:
        data = await analysis.get_repo_info(owner, repo)
        return JsonResponse(data)
    except Exception as e:
        return HttpResponse(status=404)

async def top_contributors_languages(request, owner = 'RavenTheshadow', repo = 'BTL_LTNC'):
    try:
        data = await analysis.get_top_contributors_languages(owner, repo)
        return JsonResponse(data)
    except Exception as e:
        return HttpResponse(status=404)