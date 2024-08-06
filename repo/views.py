from django.shortcuts import render
from django.http import JsonResponse
from .src.analysis import repo_analysis as analysis

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