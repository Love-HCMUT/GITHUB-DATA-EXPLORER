from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render 
from .src.analysis import analysisUser 
from .src.analysis import analysisdata
from .src.fetch import getdata
from .src.analysis import user_analysis as analysis


# Create your views here.
def Home(request):
    return render(request, 'user_index.html')


async def GetDataActivity(request): 
    try: 
        data = await analysisUser.GetUserActivies('krahets')
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)

# Create your views here.
# def Homes(request):
#     return render(request, 'index.html')

# Create your views here.
async def GetData(request):
    data = await analysisdata.gather_repo_data('KietCSE')
    # print(data)
    return JsonResponse(data, safe=False)

async def GetMonths(request):
    data = await analysisdata.data_4months('KietCSE')
    # print(data)
    return JsonResponse(data, safe=False)

# Create your views here.
def test(request):
    return render(request, 'user_index.html')
    
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
