from django.shortcuts import render
from django.http import JsonResponse
from .src.analysis import user_analysis as analysis

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