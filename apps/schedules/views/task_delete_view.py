from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Task
from ..permissions import accessible_tasks


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    pk_url_kwarg = 'task_pk'
    http_method_names = ['delete']

    def get_queryset(self):
        return accessible_tasks(self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return JsonResponse({'success': True})