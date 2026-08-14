from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        # 古い UserCreationForm ではなく、自作の SignUpForm を使う
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home') # 必要に応じてリダイレクト先を調整
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})