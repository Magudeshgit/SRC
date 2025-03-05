from django.http import HttpResponse
from django.db.models import Q


def is_moderator(view):
    def wrapper(request, *args, **kwargs):
        print("CHECK", request.user.groups.filter(name = "Moderator"))
        if request.user.groups.filter(name = "Moderator") or request.user.is_superuser:
            return view(request, *args, **kwargs)
        else:
            return HttpResponse("Access Restricted, Please click here to go to home page <a href='/'>Home</a>")
    return wrapper