import csv
import json
import io
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import UserProfile, Workout, Exercise
from .forms import DataImportForm


@login_required
@csrf_protect
def import_data(request):
    """Import workout data from CSV, JSON, or text files"""
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = form.cleaned_data['file_type']
            data_file = form.cleaned_data['data_file']
            overwrite_existing = form.cleaned_data['overwrite_existing']
            
            try:
                # Read file content
                file_content = data_file.read().decode('utf-8')
                
                if file_type == 'csv':
                    result = import_csv_data(request.user, file_content, overwrite_existing)
                elif file_type == 'json':
                    result = import_json_data(request.user, file_content, overwrite_existing)
                elif file_type == 'txt':
                    result = import_text_data(request.user, file_content, overwrite_existing)
                
                messages.success(request, f'Successfully imported {result["imported"]} workouts and {result["exercises"]} exercises.')
                return redirect('workout_list')
                
            except Exception as e:
                messages.error(request, f'Import failed: {str(e)}')
    else:
        form = DataImportForm()
    
    return render(request, 'fitness_tracker/import_data.html', {'form': form})


@login_required
def export_data(request):
    """Export workout data in CSV, JSON, or text format"""
    file_type = request.GET.get('format', 'csv')
    
    # Get user's workouts with exercises
    workouts = request.user.workouts.all().prefetch_related('exercises')
    
    if file_type == 'csv':
        return export_csv_data(workouts)
    elif file_type == 'json':
        return export_json_data(workouts)
    elif file_type == 'txt':
        return export_text_data(workouts)
    else:
        messages.error(request, 'Invalid export format.')
        return redirect('workout_list')


def import_csv_data(user, file_content, overwrite_existing):
    """Import data from CSV format"""
    csv_reader = csv.DictReader(io.StringIO(file_content))
    imported_workouts = 0
    imported_exercises = 0
    
    # Expected CSV columns for workouts:
    # date,name,workout_type,duration,calories_burned,notes
    
    for row in csv_reader:
        try:
            # Parse date
            workout_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            
            # Check if workout exists
            existing_workout = None
            if not overwrite_existing:
                existing_workout = Workout.objects.filter(
                    user=user,
                    name=row['name'],
                    date=workout_date
                ).first()
            
            if existing_workout and not overwrite_existing:
                continue
                
            # Create or update workout
            workout_data = {
                'name': row['name'],
                'workout_type': row.get('workout_type', 'other'),
                'duration': int(row['duration']),
                'calories_burned': int(row.get('calories_burned', 0)),
                'notes': row.get('notes', ''),
                'date': workout_date
            }
            
            if existing_workout and overwrite_existing:
                for key, value in workout_data.items():
                    setattr(existing_workout, key, value)
                existing_workout.save()
                workout = existing_workout
            else:
                workout = Workout.objects.create(user=user, **workout_data)
                imported_workouts += 1
            
            # Import exercises if provided in additional columns
            if 'exercise_name' in row and row['exercise_name']:
                exercise_data = {
                    'exercise_name': row['exercise_name'],
                    'category': row.get('category', 'other'),
                    'sets': int(row.get('sets', 1)),
                    'reps': int(row.get('reps', 1)),
                    'weight': float(row.get('weight', 0)),
                    'rest_time': int(row.get('rest_time', 60)),
                    'notes': row.get('exercise_notes', '')
                }
                
                Exercise.objects.create(workout=workout, **exercise_data)
                imported_exercises += 1
                
        except (ValueError, KeyError) as e:
            raise ValidationError(f'Invalid CSV data in row: {row}. Error: {str(e)}')
    
    return {'imported': imported_workouts, 'exercises': imported_exercises}


def import_json_data(user, file_content, overwrite_existing):
    """Import data from JSON format"""
    try:
        data = json.loads(file_content)
    except json.JSONDecodeError as e:
        raise ValidationError(f'Invalid JSON format: {str(e)}')
    
    imported_workouts = 0
    imported_exercises = 0
    
    # Expected JSON structure:
    # {
    #   "workouts": [
    #     {
    #       "name": "Morning Run",
    #       "date": "2024-01-01",
    #       "workout_type": "cardio",
    #       "duration": 30,
    #       "calories_burned": 300,
    #       "notes": "Great run!",
    #       "exercises": [
    #         {
    #           "exercise_name": "Running",
    #           "category": "cardio",
    #           "sets": 1,
    #           "reps": 1,
    #           "weight": 0,
    #           "rest_time": 0
    #         }
    #       ]
    #     }
    #   ]
    # }
    
    workouts_data = data.get('workouts', [])
    
    for workout_data in workouts_data:
        try:
            # Parse date
            workout_date = datetime.strptime(workout_data['date'], '%Y-%m-%d').date()
            
            # Check if workout exists
            existing_workout = None
            if not overwrite_existing:
                existing_workout = Workout.objects.filter(
                    user=user,
                    name=workout_data['name'],
                    date=workout_date
                ).first()
            
            if existing_workout and not overwrite_existing:
                continue
            
            # Create or update workout
            workout_fields = {
                'name': workout_data['name'],
                'workout_type': workout_data.get('workout_type', 'other'),
                'duration': workout_data['duration'],
                'calories_burned': workout_data.get('calories_burned', 0),
                'notes': workout_data.get('notes', ''),
                'date': workout_date
            }
            
            if existing_workout and overwrite_existing:
                for key, value in workout_fields.items():
                    setattr(existing_workout, key, value)
                existing_workout.save()
                workout = existing_workout
                # Clear existing exercises if overwriting
                workout.exercises.all().delete()
            else:
                workout = Workout.objects.create(user=user, **workout_fields)
                imported_workouts += 1
            
            # Import exercises
            exercises_data = workout_data.get('exercises', [])
            for exercise_data in exercises_data:
                Exercise.objects.create(
                    workout=workout,
                    exercise_name=exercise_data['exercise_name'],
                    category=exercise_data.get('category', 'other'),
                    sets=exercise_data.get('sets', 1),
                    reps=exercise_data.get('reps', 1),
                    weight=exercise_data.get('weight', 0),
                    rest_time=exercise_data.get('rest_time', 60),
                    notes=exercise_data.get('notes', '')
                )
                imported_exercises += 1
                
        except (ValueError, KeyError) as e:
            raise ValidationError(f'Invalid JSON data in workout: {workout_data}. Error: {str(e)}')
    
    return {'imported': imported_workouts, 'exercises': imported_exercises}


def import_text_data(user, file_content, overwrite_existing):
    """Import data from text format"""
    lines = file_content.strip().split('\n')
    imported_workouts = 0
    imported_exercises = 0
    
    # Expected text format:
    # WORKOUT: workout_name | workout_type | date | duration | calories
    # EXERCISE: exercise_name | category | sets | reps | weight
    # EXERCISE: exercise_name | category | sets | reps | weight
    # WORKOUT: ...
    
    current_workout = None
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue
        
        try:
            if line.startswith('WORKOUT:'):
                # Parse workout line
                workout_parts = [part.strip() for part in line[8:].split('|')]
                if len(workout_parts) < 4:
                    raise ValidationError(f'Line {line_num}: Workout line must have at least 4 parts')
                
                workout_name = workout_parts[0]
                workout_type = workout_parts[1] if len(workout_parts) > 1 else 'other'
                workout_date = datetime.strptime(workout_parts[2], '%Y-%m-%d').date()
                duration = int(workout_parts[3])
                calories = int(workout_parts[4]) if len(workout_parts) > 4 else 0
                notes = workout_parts[5] if len(workout_parts) > 5 else ''
                
                # Check if workout exists
                existing_workout = None
                if not overwrite_existing:
                    existing_workout = Workout.objects.filter(
                        user=user,
                        name=workout_name,
                        date=workout_date
                    ).first()
                
                if existing_workout and not overwrite_existing:
                    current_workout = existing_workout
                    continue
                
                # Create or update workout
                workout_data = {
                    'name': workout_name,
                    'workout_type': workout_type,
                    'duration': duration,
                    'calories_burned': calories,
                    'notes': notes,
                    'date': workout_date
                }
                
                if existing_workout and overwrite_existing:
                    for key, value in workout_data.items():
                        setattr(existing_workout, key, value)
                    existing_workout.save()
                    current_workout = existing_workout
                    # Clear existing exercises if overwriting
                    current_workout.exercises.all().delete()
                else:
                    current_workout = Workout.objects.create(user=user, **workout_data)
                    imported_workouts += 1
                
            elif line.startswith('EXERCISE:'):
                if current_workout is None:
                    raise ValidationError(f'Line {line_num}: Exercise found without preceding workout')
                
                # Parse exercise line
                exercise_parts = [part.strip() for part in line[9:].split('|')]
                if len(exercise_parts) < 4:
                    raise ValidationError(f'Line {line_num}: Exercise line must have at least 4 parts')
                
                exercise_name = exercise_parts[0]
                category = exercise_parts[1] if len(exercise_parts) > 1 else 'other'
                sets = int(exercise_parts[2])
                reps = int(exercise_parts[3])
                weight = float(exercise_parts[4]) if len(exercise_parts) > 4 else 0
                rest_time = int(exercise_parts[5]) if len(exercise_parts) > 5 else 60
                notes = exercise_parts[6] if len(exercise_parts) > 6 else ''
                
                Exercise.objects.create(
                    workout=current_workout,
                    exercise_name=exercise_name,
                    category=category,
                    sets=sets,
                    reps=reps,
                    weight=weight,
                    rest_time=rest_time,
                    notes=notes
                )
                imported_exercises += 1
                
        except (ValueError, IndexError) as e:
            raise ValidationError(f'Line {line_num}: Invalid format. Error: {str(e)}')
    
    return {'imported': imported_workouts, 'exercises': imported_exercises}


def export_csv_data(workouts):
    """Export workouts to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fitness_data.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    writer.writerow([
        'date', 'name', 'workout_type', 'duration', 'calories_burned', 'notes',
        'exercise_name', 'category', 'sets', 'reps', 'weight', 'rest_time', 'exercise_notes'
    ])
    
    # Write data
    for workout in workouts:
        exercises = workout.exercises.all()
        if exercises:
            for exercise in exercises:
                writer.writerow([
                    workout.date.strftime('%Y-%m-%d'),
                    workout.name,
                    workout.workout_type,
                    workout.duration,
                    workout.calories_burned,
                    workout.notes,
                    exercise.exercise_name,
                    exercise.category,
                    exercise.sets,
                    exercise.reps,
                    exercise.weight,
                    exercise.rest_time,
                    exercise.notes
                ])
        else:
            # Workout without exercises
            writer.writerow([
                workout.date.strftime('%Y-%m-%d'),
                workout.name,
                workout.workout_type,
                workout.duration,
                workout.calories_burned,
                workout.notes,
                '', '', '', '', '', '', ''
            ])
    
    return response


def export_json_data(workouts):
    """Export workouts to JSON format"""
    data = {'workouts': []}
    
    for workout in workouts:
        workout_data = {
            'name': workout.name,
            'date': workout.date.strftime('%Y-%m-%d'),
            'workout_type': workout.workout_type,
            'duration': workout.duration,
            'calories_burned': workout.calories_burned,
            'notes': workout.notes,
            'exercises': []
        }
        
        for exercise in workout.exercises.all():
            exercise_data = {
                'exercise_name': exercise.exercise_name,
                'category': exercise.category,
                'sets': exercise.sets,
                'reps': exercise.reps,
                'weight': exercise.weight,
                'rest_time': exercise.rest_time,
                'notes': exercise.notes
            }
            workout_data['exercises'].append(exercise_data)
        
        data['workouts'].append(workout_data)
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="fitness_data.json"'
    return response


def export_text_data(workouts):
    """Export workouts to text format"""
    output = []
    output.append("# Fitness Tracker Data Export")
    output.append("# Format: WORKOUT: name | type | date | duration | calories | notes")
    output.append("#         EXERCISE: name | category | sets | reps | weight | rest_time | notes")
    output.append("")
    
    for workout in workouts:
        # Write workout line
        workout_line = f"WORKOUT: {workout.name} | {workout.workout_type} | {workout.date.strftime('%Y-%m-%d')} | {workout.duration} | {workout.calories_burned}"
        if workout.notes:
            workout_line += f" | {workout.notes}"
        output.append(workout_line)
        
        # Write exercise lines
        for exercise in workout.exercises.all():
            exercise_line = f"EXERCISE: {exercise.exercise_name} | {exercise.category} | {exercise.sets} | {exercise.reps} | {exercise.weight} | {exercise.rest_time}"
            if exercise.notes:
                exercise_line += f" | {exercise.notes}"
            output.append(exercise_line)
        
        output.append("")  # Empty line between workouts
    
    response = HttpResponse('\n'.join(output), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="fitness_data.txt"'
    return response