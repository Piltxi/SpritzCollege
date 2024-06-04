from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

from Activities.models import Course
from .forms import UserGroupForm, VisitorRegistrationForm, GroupMembershipForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, UpdateView, TemplateView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message, User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

from braces.views import GroupRequiredMixin
from .models import Profile

def group_required(group_name):
    def in_group(user):
        
        if user.is_superuser:
            return True
        
        if user.groups.filter(name="administration").exists():
            return True
        
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    
    return user_passes_test(in_group)

def register(request):
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in as: {request.user.username}!')
        return redirect('home')
    
    if request.method == 'POST':
        form = VisitorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            visitors_group, created = Group.objects.get_or_create(name='visitors')
            user.groups.add(visitors_group)
            login(request, user)
            messages.success(request, "Welcome to the world's best orange platform!!")
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
    
@login_required
def delete_all_messages(request):
    user = request.user
    
    if request.method == 'POST':
        Message.objects.filter(user=user).delete()
        messages.success(request, 'Successfully deleted all your notifications. Peace and Love!')
     
        return redirect('my_messages')
    
    return render(request, 'Profiles/messages.html')

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'Profiles/profile_update.html'
    success_url = reverse_lazy('profile_update')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'password' in self.request.POST:
            password_form = CustomPasswordChangeForm(self.request.user, self.request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(self.request, password_form.user)
                return redirect(self.success_url)
        return response

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['password_form'] = CustomPasswordChangeForm(self.request.user, self.request.POST)
        else:
            context['password_form'] = CustomPasswordChangeForm(self.request.user)
        return context

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'Profiles/password_change.html'
    success_url = reverse_lazy('profile_update')

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.info(self.request, f'Your password has been updated successfully, {self.request.user.username}! Only one thing: login once again.')
        logout(self.request)
        return redirect('login')
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'Profiles/account_confirm_delete.html'
    success_url = reverse_lazy('account_deleted')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        logout(request)
        user.delete()
        return redirect(self.success_url)
    
@login_required
def course_chat(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.course_subscriptions.filter(course=course).exists():
        return render(request, 'Profiles/course_chat.html', {'course': course})
    else:
        return redirect('course_detail', pk=course_id)