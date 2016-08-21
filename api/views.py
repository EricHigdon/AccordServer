from django.http import JsonResponse
from django.core import serializers
from .models import *

# Create your views here.
def all_churches(self):
    churches = serializers.serialize("json", Church.objects.all())
    context = {'churches':churches}
    print(churches)
    return JsonResponse(context)