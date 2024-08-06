from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render 
from .src.analysis import analysisUser

# Create your views here.
def Home(request):
    return render(request, 'index.html')


async def GetDataActivity(request): 
    try: 
        data = await analysisUser.GetUserActivies('krahets')
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(status=404)