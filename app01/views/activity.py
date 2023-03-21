from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_activity(request):
    dict = request.POST
    print(dict)
    return render(request, "add_activity.html")