from django.shortcuts import render

def home(request):
    return render(request, 'cards/home.html', {'test':'TEST'})
