from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from ..models import Project
from ..forms import ProjectForm
from django.http import Http404
import time
from django.template import loader
from django.http import HttpResponse


class ProjectCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'schedules/project_calendar.html'