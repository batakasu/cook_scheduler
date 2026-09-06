from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views import generic
from django.urls import reverse
from ..forms import ToolForm
from django.shortcuts import get_object_or_404
from ..models import Project, Tool
from django.contrib.auth.mixins import LoginRequiredMixin

class ToolDetailView(LoginRequiredMixin,generic.UpdateView):
    pk_url_kwarg = 'tool_pk'
    model = Tool
    template_name = 'schedules/tool_detail.html'
    context_object_name = 'tool'
    form_class = ToolForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tool_form'] = context['form']
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # URLの kwargs から project_pk を取得して Project オブジェクトを取り出す
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        
        # フォームの初期化引数に project を追加する
        kwargs['project'] = project
        return kwargs
    
    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk')
        return reverse_lazy('schedules:tool_list', kwargs={'project_pk': project_pk})