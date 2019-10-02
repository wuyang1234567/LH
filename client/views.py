from django.shortcuts import render

# Create your views here.
def main(request):
    return  render(request, "temp-client/main.html")
def list(request):
    return render(request, "temp-client/list.html")
def detail(request):
    return render(request, "temp-client/detail.html")

