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
    

# Create your views here.
def test(request):
    return render(request, 'repo_index.html')

async def repo_languages(request, owner = 'RavenTheshadow', repo = 'BTL_LTNC'):
    data = {}
    try:
        data = await analysis.get_percent_languages(owner, repo)
    except Exception as e:
        print(e)
        data = {
            'HTML': 100.0
        }
    finally:
        return JsonResponse(data)
    
async def repo_info(request, owner = 'RavenTheShadow', repo = 'BTL_LTNC'):
    data = await analysis.get_repo_info(owner, repo)
    return JsonResponse(data)

async def top_contributors_languages(request, owner = 'RavenTheshadow', repo = 'BTL_LTNC'):
    data = await analysis.get_top_contributors_languages(owner, repo)
    return JsonResponse(data)
    
async def languages(request, username = 'KietCSE'):
    data = {}
    try:
        data = await analysis.get_languages(username)
    except Exception as e:
        print(e)
        data = {
            'HTML': 55.0,
            'Jupyter Notebook': 22.4,
            'TeX': 7.7,
            'Python': 0.8,
            'Java': 1.9,
            'Batchfile': 0.0,
            'C++': 12.0,
            'JavaScript': 0.0   
        }
    finally:
        return JsonResponse(data)

