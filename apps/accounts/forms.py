from django import forms
from django.contrib.auth import get_user_model
from .models import CookingGroup

CustomUser = get_user_model()

class SignUpForm(forms.ModelForm):
    # パスワードを隠すため、入力欄をパスワード用に設定
    password = forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta:
        model = CustomUser
        # AbstractUserが持っている標準的なフィールドを指定
        fields = ('username', 'display_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        # パスワードをハッシュ化（暗号化）して保存する
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class GroupForm(forms.ModelForm):
    class Meta:
        model = CookingGroup
        fields = ['name', 'leader']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leader'].queryset = self.instance.members.all()

class GroupMemberForm(forms.Form):
    username = forms.CharField(label='ユーザーID')

    def __init__(self, *args, **kwargs):
        self.saved_group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            return username

        user = CustomUser.objects.filter(username=username).first()

        if user is None:
            raise forms.ValidationError('そのユーザーIDは存在しません')

        if self.saved_group.members.filter(pk=user.pk).exists():
            raise forms.ValidationError('既に参加しています')

        self.found_user = user
        return username
    
    def save(self):
        self.saved_group.members.add(self.found_user)
        return self.saved_group

class UserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'display_name']