from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import macroevent as macroevents, microevent as microevents, teammember, submission, review_question
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .decorator import is_moderator

def home(request):
    return render(request, "core/index.html")
def events(request):
    payload = macroevents.objects.all().order_by('-startdate')
    banner = payload.get(is_banner=True)
    return render(request, "core/events.html", {"events": payload, "banner": banner})
def macroeventhandler(request, macroevent):
    return render(request, f"core/events/{macroevent.lower()}.html")

@login_required
def exploremicroeventhandler(request, macroevent):
    payload = ''
    if request.method == "POST":
        category = request.POST['category']
        payload = microevents.objects.filter(Q(department__stream_of__name = category) | Q(department__dept_name="Student Research Council"), micro_of = macroevents.objects.get(eventname__icontains=macroevent))
        return render(request, f"core/events/{macroevent}_events.html", {"events": payload, "stream": category, "scroll": "bottom"})
    if request.user.yos != 'FIRST':
        payload = microevents.objects.filter(Q(department__stream_of__name = request.user.department.stream_of.name) | Q(department__dept_name="Student Research Council"), micro_of = macroevents.objects.get(eventname__icontains=macroevent))
    else:
        payload = microevents.objects.filter(Q(department__dept_name= "Science & Humanities") | Q(department__dept_name="Student Research Council"), micro_of = macroevents.objects.get(eventname__icontains=macroevent))
    return render(request, f"core/events/{macroevent.lower()}_events.html", {"events":payload, "stream": request.user.department.stream_of})

@login_required
def microeventhandler(request, macroevent, microevent):
    mi = microevents.objects.get(id=microevent)
    ma = macroevents.objects.get(eventname = macroevent)
    subcount = submission.objects.filter(macroevent=ma, microevent=mi).count()
    
    if request.method == 'POST':
        print(request.POST)

        if subcount <= mi.maximum_participation:
            if not submission.objects.filter(macroevent=ma, microevent=mi, registrar = request.user):
                partipant_names = request.POST.getlist('participantname')
                rollnos = request.POST.getlist('rollno')
                contact = request.POST['contact']
                teamname = ''
                if mi.is_team_event:
                    teamname = request.POST['teamname']
                
                # The storage has been split up to into two tables,
                # 1.) Submission - Will hold team submission
                # 2.) Team member - individual record of each team member
                submit = submission.objects.create(
                    macroevent = ma,
                    microevent = mi,
                    teamname = teamname,
                    registrar = request.user
                    )
                print("CHECK", partipant_names, request.POST)
                teammembers = []
                for i in range(len(partipant_names)):
                    if rollnos[i] != '':
                        member = teammember(teamname = teamname, 
                                roll = rollnos[i], 
                                name = partipant_names[i], 
                                contact = contact,
                                
                                submission = submit,
                                event = mi,
                                macroevent = ma,
                                attendance = False,
                                is_registrar = True if request.user.username == rollnos[i] else False
                                )
                        teammembers.append(member)
                teammember.objects.bulk_create(teammembers)
                messages.add_message(request, messages.INFO, f"<p class='font-medium text-lg'>You have been successfully registered for {mi.eventname} event.</p><p class='mt-2'>You can view your verification QR Code in your <a href='/registeredevents'><u>Registered Events</u></a> page</p>")
                return redirect(reverse('macroeventexplorer', kwargs={"macroevent": macroevent}))
            else:
                messages.add_message(request, messages.INFO, f"<p class='font-medium text-lg'>Event Already Registered. Please Check your <a class='font-medium underline' href='/registeredevents'>Registered Events</a> Page</p>")
                return render(request, f"core/events/{macroevent.lower()}_microevent.html", {"event": mi})
            "<p class='text-xl font-medium text-red-600'></p>"
        else:
            mi.registration_closed = True
            mi.save()
            return redirect(reverse('macroeventexplorer', kwargs={"macroevent": macroevent}))
            
    if mi.registration_closed:
        return redirect(reverse('macroeventexplorer', kwargs={"macroevent": macroevent}))
    
    return render(request, f"core/events/{macroevent.lower()}_microevent.html", {"event": mi})

@login_required
def registered_events(request):
    payload = teammember.objects.filter(roll=request.user.username, is_registrar = True)
    return render(request, 'core/registeredevents.html', {"events": payload})

@login_required
def attendance_handler(request, submission_id):
    try:
        _submission = submission.objects.get(id=submission_id)
        members = teammember.objects.filter(submission__id = submission_id)
        team_lead = members.get(is_registrar = True)

        if not team_lead.attendance:
            members_attended = []
            for member in members:
                member.attendance = True
                members_attended.append(member)
            teammember.objects.bulk_update(members_attended, ['attendance'])
            return JsonResponse({"status": True,"event":_submission.microevent.eventname,"teamname": _submission.teamname, "participant": _submission.registrar.full_name, "roll":_submission.registrar.username})
        else:
            return JsonResponse({"status": False, "message": "This QR code has already been scanned."})
    except ObjectDoesNotExist:
        return JsonResponse({"status": False, "message": "Invalid, Registration not found"})

@login_required
@is_moderator
def attendance_scanner(request):
    return render(request, 'core/attendancescanner.html')

@login_required
def event_review(request, event_id):
    try:
        event = microevents.objects.get(id=event_id)
        teammember.objects.filter(is_registrar = True, roll = request.user.username)
        questions = review_question.objects.filter(event = event)
        
    except ObjectDoesNotExist:
        return redirect('/')
    
    
    return render(request, "core/events/technofete'25_event_review.html")

