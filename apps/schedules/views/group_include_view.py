from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ..services import include_group
from ..permissions import accessible_projects
from apps.accounts.permissions import accessible_groups

class GroupIncludeView(LoginRequiredMixin, View):
    def get(self, request, project_pk):
        project = get_object_or_404(
            accessible_projects(request.user),
            pk = project_pk
        )

        context = {
            'project': project,
            'groups': accessible_groups(request.user),
        }

        return render(request, 'schedules/group_include.html', context)

    def post(self, request, project_pk):
        project = get_object_or_404(
            accessible_projects(request.user),
            pk=project_pk
        )
        group = get_object_or_404(
            accessible_groups(request.user),
            pk=request.POST.get('group_pk')
        )
        include_group(
            project,
            group
        )

        return redirect('schedules:membership_list', project_pk=project.pk)