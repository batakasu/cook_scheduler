from django.views import generic
from django.urls import reverse
from ..models import CookingGroup
from ..forms import GroupForm, GroupMemberForm
from ..permissions import accessible_groups
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    pk_url_kwarg = 'group_pk'
    model = CookingGroup
    template_name = 'accounts/group_update.html'
    context_object_name = 'group'
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_form'] = GroupMemberForm(group=self.object)

        return context

    def get_queryset(self):
        groups = accessible_groups(self.request.user)
        return groups
    
    def get_success_url(self):
        return reverse('accounts:profile')

@login_required
def add_member(request, group_pk):
    group = get_object_or_404(
        accessible_groups(request.user),
        pk=group_pk
    )

    if request.method == 'POST':
        member_form = GroupMemberForm(
            request.POST,
            group=group
        )

        if member_form.is_valid():
            member_form.save()

            return redirect(
                'accounts:group_update',
                group_pk=group.pk
            )

        return render(
            request,
            'accounts/group_update.html',
            {
                'group': group,
                'form': GroupForm(instance=group),
                'member_form': member_form,
            }
        )

@login_required
@require_POST
def remove_member(request, group_pk):
    group = get_object_or_404(
        accessible_groups(request.user),
        pk=group_pk
    )

    if request.method == 'POST':
        username = request.POST.get('username')

        member = get_object_or_404(
            group.members,
            username=username
        )

        # リーダーは削除させない
        if member == group.leader:
            return redirect(
                'accounts:group_update',
                group_pk=group.pk
            )

        group.members.remove(member)

        # 自分を削除したら
        if member == request.user:
            return redirect('accounts:profile')

        return redirect(
            'accounts:group_update',
            group_pk=group.pk
        )
