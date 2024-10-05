from django.shortcuts import render

def test(request):
    return render(request, 'card/test.html', {'proba': 'PROBA'})

