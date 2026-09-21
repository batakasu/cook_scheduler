from ..forms import ProjectForm
from ..models import Project, Membership, Task
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, time, datetime
from django.urls import reverse

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'schedules/project_create.html'

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
        
        membership = Membership.objects.create(
            project=self.object,
            user=self.request.user
        )
        Task.objects.create(
            project=self.object,
            membership=membership,
            title='手を洗う',
            start_offset=0,
            duration=5
        )
        
        return response

    def get_success_url(self):
        return reverse(
            'schedules:project_detail',
            kwargs={'project_pk': self.object.pk}
        )