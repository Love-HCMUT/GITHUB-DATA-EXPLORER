from django.http import JsonResponse
from django.shortcuts import render
from .src.analysis import analysis2
from django.template import loader
from django.http import HttpResponse
from .src.analysis import analysisdata
from .src.fetch import getdata

# Create your views here.
async def LoadDataOrg(request): 
    data = await analysis2.GetDataOrg('microsoft')
    return JsonResponse(data)


def LoadTemplate(request):
    return render(request, 'org_index.html')

# Create your views here.
def Home(request):
    return render(request, 'index1.html')

# Create your views here.
async def GetData(request):
    data = await analysisdata.gather_repo_data('TickLabVN')
    # print(data)
    return JsonResponse(data, safe=False)

