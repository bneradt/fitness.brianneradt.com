from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import WorkoutSession, PullupType
from .forms import WorkoutSessionForm
import json

class WorkoutSessionListView(LoginRequiredMixin, ListView):
    model = WorkoutSession
    template_name = 'workoutlog/workoutsession_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).order_by('-date')

class WorkoutSessionDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutSession
    template_name = 'workoutlog/workoutsession_detail.html'
    context_object_name = 'session'

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = 'workoutlog/workoutsession_form.html'

    def get_success_url(self):
        # Trigger celebration on the list page after saving a new workout.
        return reverse_lazy('workoutlog:view_workout_sessions') + '?celebrate=1'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutSessionUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = 'workoutlog/workoutsession_form.html'
    success_url = reverse_lazy('workoutlog:view_workout_sessions')

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

class WorkoutSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutSession
    context_object_name = 'session'
    template_name = 'workoutlog/workoutsession_confirm_delete.html'
    success_url = reverse_lazy('workoutlog:view_workout_sessions')

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

class WorkoutSessionPlotView(LoginRequiredMixin, TemplateView):
    template_name = 'workoutlog/workoutsession_plot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = WorkoutSession.objects.filter(user=self.request.user).order_by('date')
        labels = [session.date.strftime('%Y-%m-%d') for session in sessions]
        pullups = [session.total_pullups if session.pullup_type == PullupType.PULLUPS else 0 for session in sessions]
        chinups = [session.total_pullups if session.pullup_type == PullupType.CHINUPS else 0 for session in sessions]
        neutral = [session.total_pullups if session.pullup_type == PullupType.NEUTRAL else 0 for session in sessions]
        pushups = [session.total_pushups for session in sessions]
        context['labels_json'] = json.dumps(labels)
        context['pullups_json'] = json.dumps(pullups)
        context['chinups_json'] = json.dumps(chinups)
        context['neutral_json'] = json.dumps(neutral)
        context['pushups_json'] = json.dumps(pushups)
        return context
