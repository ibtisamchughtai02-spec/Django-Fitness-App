from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg, Max, F
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import json
import csv
from datetime import datetime, timedelta
from .models import UserProfile, Workout, Exercise
from .forms import (
    CustomUserCreationForm, UserProfileForm, WorkoutForm, 
    ExerciseForm, QuickWorkoutForm, DataImportForm
)
from .data_utils import import_data, export_data


# Authentication Views
def register(request):
    """User registration view with profile creation"""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Profile is automatically created by signal, so just update it
            profile = user.profile
            profile_data = profile_form.cleaned_data
            profile.age = profile_data.get('age')
            profile.weight = profile_data.get('weight')
            profile.height = profile_data.get('height')
            profile.activity_level = profile_data.get('activity_level')
            profile.fitness_goal = profile_data.get('fitness_goal')
            profile.save()
            
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_login(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


# Dashboard and Profile Views
@login_required
def dashboard(request):
    """Main dashboard view with statistics and recent activity"""
    user = request.user
    
    # Get user profile or create if doesn't exist
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, age=25, weight=70, height=170)
    
    # Calculate statistics
    total_workouts = user.workouts.count()
    total_exercises = Exercise.objects.filter(workout__user=user).count()
    
    # Last 30 days statistics
    last_30_days = timezone.now().date() - timedelta(days=30)
    recent_workouts = user.workouts.filter(date__gte=last_30_days)
    workouts_this_month = recent_workouts.count()
    total_calories = recent_workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    avg_duration = recent_workouts.aggregate(Avg('duration'))['duration__avg'] or 0
    
    # Recent activity
    recent_workouts_list = user.workouts.all()[:5]
    
    # Workout type distribution
    workout_types = user.workouts.values('workout_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'profile': profile,
        'total_workouts': total_workouts,
        'total_exercises': total_exercises,
        'workouts_this_month': workouts_this_month,
        'total_calories': total_calories,
        'avg_duration': round(avg_duration, 1),
        'recent_workouts': recent_workouts_list,
        'workout_types': workout_types,
    }
    
    return render(request, 'fitness_tracker/dashboard.html', context)


@login_required
def profile_view(request):
    """User profile view and edit"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, age=25, weight=70, height=170)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Calculate BMI and additional stats
    bmi = profile.calculate_bmi()
    bmi_category = profile.get_bmi_category()
    
    context = {
        'form': form,
        'profile': profile,
        'bmi': bmi,
        'bmi_category': bmi_category,
    }
    
    return render(request, 'fitness_tracker/profile.html', context)


# Workout CRUD Views
@login_required
def workout_list(request):
    """List all workouts with filtering and pagination"""
    workouts = request.user.workouts.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        workouts = workouts.filter(
            Q(name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # Filter by workout type
    workout_type = request.GET.get('type')
    if workout_type:
        workouts = workouts.filter(workout_type=workout_type)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        workouts = workouts.filter(date__gte=date_from)
    if date_to:
        workouts = workouts.filter(date__lte=date_to)
    
    # Pagination
    paginator = Paginator(workouts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get workout types for filter dropdown
    workout_types = Workout.WORKOUT_TYPES
    
    context = {
        'page_obj': page_obj,
        'workout_types': workout_types,
        'search_query': search_query,
        'selected_type': workout_type,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'fitness_tracker/workout_list.html', context)


@login_required
def workout_detail(request, pk):
    """Detailed view of a specific workout"""
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    exercises = workout.exercises.all()
    
    # Calculate totals
    total_sets = workout.get_total_sets()
    total_volume = sum(exercise.get_total_volume() for exercise in exercises)
    
    context = {
        'workout': workout,
        'exercises': exercises,
        'total_sets': total_sets,
        'total_volume': total_volume,
    }
    
    return render(request, 'fitness_tracker/workout_detail.html', context)


@login_required
@csrf_protect
def workout_create(request):
    """Create a new workout"""
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Workout created successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm()
    
    return render(request, 'fitness_tracker/workout_form.html', {
        'form': form,
        'title': 'Create New Workout'
    })


@login_required
@csrf_protect
def workout_edit(request, pk):
    """Edit an existing workout"""
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout updated successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm(instance=workout)
    
    return render(request, 'fitness_tracker/workout_form.html', {
        'form': form,
        'workout': workout,
        'title': 'Edit Workout'
    })


@login_required
@require_POST
@csrf_protect
def workout_delete(request, pk):
    """Delete a workout (POST-only for security)"""
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    workout_name = workout.name
    workout.delete()
    messages.success(request, f'Workout "{workout_name}" deleted successfully!')
    return redirect('workout_list')


# Exercise CRUD Views
@login_required
@csrf_protect
def exercise_create(request, workout_pk):
    """Add exercise to a workout"""
    workout = get_object_or_404(Workout, pk=workout_pk, user=request.user)
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            messages.success(request, 'Exercise added successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = ExerciseForm()
    
    return render(request, 'fitness_tracker/exercise_form.html', {
        'form': form,
        'workout': workout,
        'title': 'Add Exercise'
    })


@login_required
@csrf_protect
def exercise_edit(request, pk):
    """Edit an exercise"""
    exercise = get_object_or_404(Exercise, pk=pk, workout__user=request.user)
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exercise updated successfully!')
            return redirect('workout_detail', pk=exercise.workout.pk)
    else:
        form = ExerciseForm(instance=exercise)
    
    return render(request, 'fitness_tracker/exercise_form.html', {
        'form': form,
        'exercise': exercise,
        'workout': exercise.workout,
        'title': 'Edit Exercise'
    })


@login_required
@require_POST
@csrf_protect
def exercise_delete(request, pk):
    """Delete an exercise (POST-only for security)"""
    exercise = get_object_or_404(Exercise, pk=pk, workout__user=request.user)
    workout_pk = exercise.workout.pk
    exercise_name = exercise.exercise_name
    exercise.delete()
    messages.success(request, f'Exercise "{exercise_name}" deleted successfully!')
    return redirect('workout_detail', pk=workout_pk)


# Quick Workout Views
@login_required
@csrf_protect
def quick_workout(request):
    """Quick workout logging for mobile/fast entry"""
    if request.method == 'POST':
        form = QuickWorkoutForm(request.POST)
        if form.is_valid():
            workout = Workout.objects.create(
                user=request.user,
                name=form.cleaned_data['workout_name'],
                workout_type=form.cleaned_data['workout_type'],
                duration=form.cleaned_data['duration'],
                calories_burned=form.cleaned_data.get('calories', 0),
                date=timezone.now().date()
            )
            messages.success(request, 'Quick workout logged successfully!')
            return redirect('workout_list')
    else:
        form = QuickWorkoutForm()
    
    return render(request, 'fitness_tracker/quick_workout.html', {'form': form})


# Progress and Statistics Views
@login_required
def progress_view(request):
    """Progress tracking and statistics"""
    user = request.user
    
    # Last 12 weeks of data
    twelve_weeks_ago = timezone.now().date() - timedelta(weeks=12)
    workouts = user.workouts.filter(date__gte=twelve_weeks_ago).order_by('date')
    
    # Weekly aggregation
    weekly_data = []
    for i in range(12):
        week_start = twelve_weeks_ago + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        week_workouts = workouts.filter(date__range=[week_start, week_end])
        
        weekly_data.append({
            'week': week_start.strftime('%Y-W%U'),
            'workouts': week_workouts.count(),
            'total_duration': week_workouts.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_calories': week_workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
        })
    
    # Workout types distribution
    workout_type_stats = workouts.values('workout_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    total_workouts = workouts.count()
    workout_types = {}
    for stat in workout_type_stats:
        workout_types[stat['workout_type']] = {
            'count': stat['count'],
            'percentage': round((stat['count'] / total_workouts * 100) if total_workouts > 0 else 0, 1)
        }
    
    # Exercise frequency
    exercise_stats = Exercise.objects.filter(
        workout__user=user,
        workout__date__gte=twelve_weeks_ago
    ).values('exercise_name').annotate(
        count=Count('id'),
        total_volume=Sum(F('sets') * F('reps') * F('weight'))
    ).order_by('-count')[:10]
    
    context = {
        'weekly_data': weekly_data,
        'workout_types': workout_types,
        'exercise_stats': exercise_stats,
    }
    
    return render(request, 'fitness_tracker/progress.html', context)


# Utility views for reusable functions (as required)
def get_user_workout_statistics(user, days=30):
    """Reusable function to get user workout statistics"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    workouts = user.workouts.filter(date__range=[start_date, end_date])
    
    return {
        'total_workouts': workouts.count(),
        'total_duration': workouts.aggregate(Sum('duration'))['duration__sum'] or 0,
        'total_calories': workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
        'avg_duration': workouts.aggregate(Avg('duration'))['duration__avg'] or 0,
        'workout_types': workouts.values('workout_type').annotate(count=Count('id')),
    }


def get_exercise_leaderboard(user, category=None):
    """Reusable function to get exercise leaderboard"""
    exercises = Exercise.objects.filter(workout__user=user)
    
    if category:
        exercises = exercises.filter(category=category)
    
    return exercises.values('exercise_name').annotate(
        total_volume=Sum(F('sets') * F('reps') * F('weight')),
        total_reps=Sum(F('sets') * F('reps')),
        max_weight=Max('weight'),
        frequency=Count('id')
    ).order_by('-total_volume')
