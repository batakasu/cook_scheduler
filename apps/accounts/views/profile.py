from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from ..models import CookingGroup

class profile(LoginRequiredMixin, TemplateView) :
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info'] = self.request.user

        context['groups'] = self.request.user.cooking_groups.all()
        return context


@login_required
@require_POST
def group_create(request):
    group = CookingGroup.objects.create(
        leader=request.user
    )

    group.members.add(request.user)

    return redirect(
        'accounts:group_update',
        group_pk=group.pk
    )