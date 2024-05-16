from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import UserGroupForm, VisitorRegistrationForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            # Salva l'utente
            user = form.save()

            # Aggiungi l'utente al gruppo "visitors"
            visitors_group, created = Group.objects.get_or_create(name='visitors')
            user.groups.add(visitors_group)

            # Effettua l'accesso automatico dell'utente
            login(request, user)

            # Reindirizza l'utente alla home
            return redirect('home')
    else:
        form = VisitorRegistrationForm()
    return render(request, 'Profiles/register.html', {'form': form})

# @user_passes_test(lambda u: u.is_superuser)
def manage_user_groups(request):
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            groups = form.cleaned_data['groups']
            user.groups.set(groups)  # Imposta i gruppi selezionati per l'utente
            return redirect('manage_user_groups')
    else:
        form = UserGroupForm()
    return render(request, 'Profiles/manage_user_groups.html', {'form': form})
