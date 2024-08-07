from django.http import JsonResponse
from django.shortcuts import render
from .src.analysis import analysis2
from django.template import loader
from django.http import HttpResponse
from .src.analysis import analysisdata
from .src.fetch import getdata
from .src.analysis import org_analysis as analysis
from ErrorHandler.exceptionHandler import HandlerException

# Create your views here.
async def LoadDataOrg(request): 
    try: 
        data = await analysis2.GetDataOrg('soft')
        return JsonResponse(data)
    except Exception as e:
        return HandlerException(e)


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

# Create your views here.
def test(request):
    return render(request, 'org_index.html')

async def languages(request, orgname = 'TickLabVN'):
    data = {}
    try:
        data = await analysis.get_languages(orgname)
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
    
async def contributions(request, orgname = 'TickLabVN'):
    data = await analysis.get_org_contributions_last_6_months(orgname)
    return JsonResponse(data)

