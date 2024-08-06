from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render 
from .src.analysis import analysisUser 
from .src.analysis import analysisdata
from .src.fetch import getdata


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
