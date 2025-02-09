from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'mainapp/homepage.html')

def analyze(request):
    return render(request, 'mainapp/analyze.html')