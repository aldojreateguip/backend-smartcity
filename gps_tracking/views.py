from django.http import HttpResponse
from tcp_server import start_tcp_server

def start_server_view(request):
    start_tcp_server()
    return HttpResponse("TCP server started")