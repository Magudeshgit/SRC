"""projectX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import *
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    path('', home, name="home"),
    path('signup/', signup),
    path('signin/', signin),
    path('forgot_password/', password_reset.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset-mail-sent/', passwordResetMailSent, name='passwordresetmailsent'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"), name="password_reset_complete"),
    path('registeredevents/', registered_events),
    path('attendancehandler/<int:submission_id>/', attendance_handler),
    path('attendancescanner/', attendance_scanner),
    
    
    path('events/', events),
    path('events/<str:macroevent>/', macroeventhandler, name='macroevent'),
    path('events/<str:macroevent>/explore/', exploremicroeventhandler, name="macroeventexplorer"),
    path('events/<str:macroevent>/<str:microevent>/', microeventhandler, name="microeventdetails"),
    path('events/<str:macroevent>/download/<int:eventid>', additional_file_download, name="downloadadditionalfile"),
    path('event_review/<int:event_id>/', event_review),
    
    path('logout/', user_logout)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
