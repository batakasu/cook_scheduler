from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SignUpForm(forms.ModelForm):
    # パスワードを隠すため、入力欄をパスワード用に設定
    password = forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta:
        model = CustomUser
        # AbstractUserが持っている標準的なフィールドを指定
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        # パスワードをハッシュ化（暗号化）して保存する
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user