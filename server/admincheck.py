
from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin
class LoginAuth(MiddlewareMixin):
    def process_request(self, request):
        url = request.path
        if url.startswith("/server") and not url == ("/server/login"):
            if request.session.get('username'):
                pass
            else:
                print(request.POST.get("password"))
                if url == "/server/loginHandler" and request.POST.get("password") != None:
                    pass
                else:
                    return redirect("/server/login")