from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class M1(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info == '/login/':
            return

        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect('http://127.0.0.1:8000/login')