from django.http import JsonResponse
from django.shortcuts import render
from .src.analysis import analysis2

# Create your views here.
async def LoadDataOrg(request): 
    data = await analysis2.GetDataOrg('microsoft')
    return JsonResponse(data)


def LoadTemplate(request):
    return render(request, 'org_index.html')