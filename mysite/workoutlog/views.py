from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import WorkoutSession
from .forms import WorkoutSessionForm

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
    success_url = reverse_lazy('workoutlog:view_workout_sessions')

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
    template_name = 'workoutlog/workoutsession_confirm_delete.html'
    success_url = reverse_lazy('workoutlog:view_workout_sessions')

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)
