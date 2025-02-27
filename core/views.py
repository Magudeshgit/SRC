from django.shortcuts import render

def home(request):
    return render(request, "core/index.html")
def events(request):
    return render(request, "core/events.html")
def macroeventhandler(request, macroevent):
    return render(request, f"core/{macroevent.lower()}.html")