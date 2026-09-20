from ..forms import ProjectForm
from ..models import Project, Membership
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import date, time, datetime

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'schedules/project_create.html'
    success_url = reverse_lazy('schedules:project_list')

    def get_initial(self):
        initial = super().get_initial()

        selected_date = self.request.GET.get('date')
        # カレンダーの日付選択からなら、その日の9時で初期化
        if selected_date:
            selected_date = date.fromisoformat(selected_date)
            default_time = time(9, 0)

            initial['scheduled_at'] = datetime.combine(selected_date, default_time)

        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        
        Membership.objects.create(
            project=self.object,
            user=self.request.user
        )
        
        return response