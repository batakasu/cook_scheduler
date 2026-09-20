from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProjectCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'schedules/project_calendar.html'