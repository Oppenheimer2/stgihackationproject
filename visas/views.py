from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import amrika
from .serializers import amrikaSerializer


@api_view(['GET'])
def mean(request):
    
    data = amrika.objects.all()
    serialized_salaries = amrikaSerializer(data ,many = True).data
    total_salary = 0
    num_salaries = len(serialized_salaries)
    for entry in serialized_salaries:
        total_salary += entry['salary']
    mean_salary = total_salary / num_salaries if num_salaries != 0 else 0
    
    return Response({'mean_salary': mean_salary})
@api_view(['GET'])
def count(request):

    data = amrika.objects.all()
    serialized_salaries = amrikaSerializer(data ,many = True).data

    num_salaries = len(serialized_salaries)
    return Response({'count': num_salaries})
@api_view(['GET'])
def median(request):

    data = amrika.objects.all()
    serialized_salaries = amrikaSerializer(data ,many = True).data

    salaries = [entry['salary'] for entry in serialized_salaries]

    salaries.sort()


    num_salaries = len(salaries)
    if num_salaries % 2 == 0:

        median_salary = (salaries[num_salaries // 2 - 1] + salaries[num_salaries // 2]) / 2
    else:

        median_salary = salaries[num_salaries // 2]
    return Response({'median': median_salary})
@api_view(['GET'])
def percentile(request):
    percen = int(request.GET.get('percentile', None))
    val = percen/100
    data = amrika.objects.all()
    serialized_salaries = amrikaSerializer(data ,many = True).data
    salaries = [entry['salary'] for entry in serialized_salaries]
    # Sort the salary values
    salaries.sort()
    index = int(val * len(salaries))
    return Response({f'{percen}th_percentile_salary':salaries[index]})

    