from django.views.generic import ListView
from ..models import Project

class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    
    def get_queryset(self):
        self.sort_type = self.request.GET.get('sort', 'new')
        
        if self.sort_type == 'old':
            return Project.objects.order_by('scheduled_at')  # 古い順
        elif self.sort_type == 'title':
            return Project.objects.order_by('title')         # タイトル順
        else:
            return Project.objects.order_by('-scheduled_at') # 新しい順（デフォルト）

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.sort_type
        return context