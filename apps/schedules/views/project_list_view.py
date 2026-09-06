from django.views.generic import ListView
from ..models import Project
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    
    def get_queryset(self):
        self.sort_type = self.request.GET.get('sort', 'new')
        projects = Project.objects.filter(members__user=self.request.user)
        
        if self.sort_type == 'old':
            return projects.order_by('scheduled_at')  # 古い順
        elif self.sort_type == 'title':
            return projects.order_by('title')         # タイトル順
        else:
            return projects.order_by('-scheduled_at') # 新しい順（デフォルト）

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.sort_type
        return context