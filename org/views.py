from django.http import JsonResponse
from django.shortcuts import render
from .src.analysis import analysis2
from django.template import loader
from django.http import HttpResponse
from .src.analysis import analysisdata
from .src.fetch import getdata
from .src.analysis import org_analysis as analysis

# Create your views here.
def LoadTemplate(request):
    return render(request, 'org_index.html')

async def LoadDataOrg(request, orgname):
    try:
        data = await analysis2.GetDataOrg(orgname)
        return JsonResponse(data, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)

# Create your views here.
async def GetData(request, orgname):
    try:
        data = await analysisdata.gather_repo_data(orgname)
        return JsonResponse(data, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)

async def languages(request, orgname):
    try:
        data = await analysis.get_languages(orgname)
        return JsonResponse(data, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)
    
async def contributions(request, orgname):
    try:
        data = await analysis.get_org_contributions_last_6_months(orgname)
        return JsonResponse(data, status = 200)
    except Exception as e:
        return HttpResponse(status = 404)

