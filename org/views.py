from django.shortcuts import render
from django.http import JsonResponse
from .src.analysis import org_analysis as analysis

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