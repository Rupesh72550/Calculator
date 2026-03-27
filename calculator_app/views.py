from django.shortcuts import render
from django.http import JsonResponse
from .utils import evaluate
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def calculate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expression = data.get('expression', '')
            result = evaluate(expression)
            return JsonResponse({'success': True, 'result': result})
        except ZeroDivisionError:
            return JsonResponse({'success': False, 'error': 'Div By Zero'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e) or 'Error'})
    return JsonResponse({'success': False, 'error': 'Invalid Request'})
