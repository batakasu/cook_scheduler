from django import forms
from .models import Project, Task, Membership, Tool
from apps.accounts.models import CustomUser
from django.forms import inlineformset_factory

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'scheduled_at']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MembershipForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーID', required=False)

    class Meta:
        model = Membership
        fields = ['username', 'guest_name']
    
    def __init__(self, *args, **kwargs):
        self.saved_project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            return username
        
        user = CustomUser.objects.filter(username=username).first()
        
        if user is None:
            raise forms.ValidationError('そのユーザーIDは存在しません')
        
        self.found_user = user
        return username
    
    def save(self, commit=True):
        self.instance.project = self.saved_project

        if hasattr(self, 'found_user'):
            self.instance.user = self.found_user

        return super().save(commit=commit)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'membership', 'duration', 'leave']    

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project is not None:
            self.fields['membership'].queryset = Membership.objects.filter(project=project)
        else:
            self.fields['membership'].queryset = Membership.objects.none()

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description']

    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

TaskFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskForm,
    extra=1,
    can_delete=True
)
