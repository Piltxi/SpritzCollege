from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .forms import UserGroupForm, VisitorRegistrationForm, ProfileUpdateForm, GroupMembershipForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message, User

from braces.views import GroupRequiredMixin
from .models import Profile

def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)

def register(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in as: {request.user.username}!')
        return redirect('home')
    
    if request.method == 'POST':
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            visitors_group, created = Group.objects.get_or_create(name='visitors')
            user.groups.add(visitors_group)
            login(request, user)    
            return redirect('home')
    else:
        form = VisitorRegistrationForm()
    
    return render(request, 'Profiles/register.html', {'form': form, 'title': "Submit - SpritzCollege"})


class ManageUserGroupsView(GroupRequiredMixin, View):
    group_required = 'administration'
    form_class = UserGroupForm
    template_name = "Activities/master_activity.html"
    success_url = reverse_lazy("list_events")

    def get(self, request):
        form = UserGroupForm()
        return render(request, 'Activities/master_activity.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, user_instance=request.user)
        if form.is_valid():
            user = form.cleaned_data['user']
            groups = form.cleaned_data['groups']
            user.groups.set(groups)
            
            return redirect('manage_user_groups')
        
        return render(request, 'Activities/master_activity.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'control_panel.html', {'form': form, 'title': "My Profile"})

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'Profiles/messages.html'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        message_count = queryset.count()
        print(f"Number of messages: {message_count}")
        context['message_count'] = message_count
        context['title'] = "My Notifications - SpritzCollege"
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'A/profile_form.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy("profile")

@group_required('administration')
def manage_group_membership(request):
    if request.method == 'POST':
        form = GroupMembershipForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group']
            action = form.cleaned_data['action']
            if action == 'add':
                user.groups.add(group)
            elif action == 'remove':
                user.groups.remove(group)
            messages.success(request, f'Successfully updated the user <{user.username}> be careful not to do any more strange things!')
            return redirect('manage_membership')
    else:
        form = GroupMembershipForm()
    return render(request, 'Profiles/manage_membership.html', {'form': form})

#! deprecated _________________________
class MyPanelView(LoginRequiredMixin, TemplateView):
    template_name = "Profiles/my_panel.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = f"{user.username} \u2192 Control Room"
        print ("ctx: ", context['title'])
        return context
#! deprecated _________________________
    
@login_required
def delete_all_messages(request):
    user = request.user
    print ("\n\nciao ciao ciao\n\n")
    
    if request.method == 'POST':
        Message.objects.filter(user=user).delete()
        messages.success(request, 'Successfully deleted all your notifications. Peace and Love!')
     
        return redirect('my_messages')
    
    return render(request, 'Profiles/messages.html')