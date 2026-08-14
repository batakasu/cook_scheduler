from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from ..models import Task

class delete_task(DeleteView):
    model = Task
    pk_url_kwarg = 'task_pk'

    # 削除成功時にJSONを返すように上書き
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
    
    # 通常のGETアクセスなどの場合は必要に応じて対応（APIとして使うならdeleteメソッドだけでOK）
    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)