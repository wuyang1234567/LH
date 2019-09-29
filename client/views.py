from django.shortcuts import render

# Create your views here.
def main(request):
    return  render(request,"main.html")
def list(request):
    return render(request, "list.html")
def detail(request):
    return render(request, "detail.html")