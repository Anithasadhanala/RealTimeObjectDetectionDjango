from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from app.camera import openCamera


def index(request):
    return render(request,"index.html")

def cam(request):
    return render(request,"cam.html")
            
def generate(camera):
    while True:
        frame = camera
        if(frame is not None):
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def open_cam(request):
    return openCamera().get_frame()

    

