from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.schedules.models import Project
from django.shortcuts import get_object_or_404
from django.utils import timezone

class HomeView(LoginRequiredMixin,TemplateView) :
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        project = Project.objects.filter(members__user=self.request.user).filter(scheduled_at__gte=now)
        context['project'] = project.order_by("scheduled_at").first()
        return context