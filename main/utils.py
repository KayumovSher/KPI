# myapp/permissions.py
from .models import KpiModel, WorkModel, DeadlineModel, SportDateModel, SportModel, MeetingDateModel, MeetingModel
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

class IsAdminOrReadOnly:
    def __init__(self, view_func):
        self.view_func = view_func

    def __call__(self, request, *args, **kwargs):
        if request.method == 'GET' or request.user.is_staff:
            return self.view_func(request, *args, **kwargs)
        if request.user.is_authenticated == False:
            return login_required(self.view_func, login_url='login')(request, *args, **kwargs) 
        elif request.method == 'POST':
            if request.user.is_authenticated and request.user.is_staff:
                return self.view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to perform this action.")


def is_admin(user):
    return user.is_authenticated and user.is_staff

def change_score(work_id=None, deadline_id=None, kpi_id=None, score=0):
    kpi_user = KpiModel.objects.get(id=kpi_id)
    dead_obj = DeadlineModel.objects.get(id=deadline_id)
    if work_id == 0:
            WorkModel.objects.create(deadline=dead_obj, score=score, kpi=kpi_user).save()
            return redirect('/all_works/')
        
    work = get_object_or_404(WorkModel, id=work_id)
    work.score = score
    work.save()
    
    
def change_sport_score(sport_id=None, sport_date_id=None, kpi_id=None, score=0):
    kpi_user = KpiModel.objects.get(id=kpi_id)
    sport_date_obj = SportDateModel.objects.get(id=sport_date_id)
    if sport_id == 0 or sport_id == 'None':
            SportModel.objects.create(sport_date=sport_date_obj, score=score, kpi=kpi_user).save()
            return redirect('/all_sports/')
        
    sport = get_object_or_404(SportModel, id=sport_id)
    sport.score = score
    sport.save()
    
def change_meeting_score(meeting_id=None, meeting_date_id=None, kpi_id=None, score=0):
    kpi_user = KpiModel.objects.get(id=kpi_id)
    meeting_date_obj = MeetingDateModel.objects.get(id=meeting_date_id)
    if meeting_id == 0 or meeting_id == 'None':
            MeetingModel.objects.create(meeting_date=meeting_date_obj, score=score, kpi=kpi_user).save()
            return redirect('/all_sports/')
        
    meeting = get_object_or_404(MeetingModel, id=meeting_id)
    meeting.score = score
    meeting.save()