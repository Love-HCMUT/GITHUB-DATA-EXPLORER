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


async def GetDataActivity(request, username, TOKEN): 
    try: 
        data = await analysisUser.GetUserActivies(username, TOKEN)
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)


# Create your views here.
async def GetData(request, username, TOKEN):
    try:
        data = await analysisdata.gather_repo_data(username, TOKEN)
        return JsonResponse(data, safe=False, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)

async def GetMonths(request, username, TOKEN):
    try:
        data = await analysisdata.data_4months(username, TOKEN)
        return JsonResponse(data, safe=False, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)

    
async def languages(request, username, TOKEN):
    data = {}
    try:
        data = await analysis.get_languages(username, TOKEN)
        return JsonResponse(data, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)
