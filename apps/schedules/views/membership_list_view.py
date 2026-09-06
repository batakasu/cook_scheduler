from django.views.generic import ListView
from apps.schedules.models import Membership, Project
from django.shortcuts import get_object_or_404

class MembershipListView(ListView):
    model = Membership
    template_name = 'schedules/membership_list.html'
    context_object_name = 'membership_list'

    def get_queryset(self):
        # URLに含まれる project_pk を取得し、そのプロジェクトのメンバーに絞り込む
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return Membership.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレート側でプロジェクト情報も使えるように渡しておく
        context['project'] = self.project
        return context