from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with fitness-related information"""
    
    ACTIVITY_LEVELS = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('lightly_active', 'Lightly Active (light exercise 1-3 days/week)'),
        ('moderately_active', 'Moderately Active (moderate exercise 3-5 days/week)'),
        ('very_active', 'Very Active (hard exercise 6-7 days/week)'),
        ('extremely_active', 'Extremely Active (very hard exercise, physical job)')
    ]
    
    FITNESS_GOALS = [
        ('lose_weight', 'Lose Weight'),
        ('gain_muscle', 'Gain Muscle'),
        ('maintain_weight', 'Maintain Weight'),
        ('improve_endurance', 'Improve Endurance'),
        ('general_fitness', 'General Fitness')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(13), MaxValueValidator(120)],
        help_text="Age must be between 13 and 120 years"
    )
    weight = models.FloatField(
        validators=[MinValueValidator(30.0), MaxValueValidator(500.0)],
        help_text="Weight in kg (30-500 kg)"
    )
    height = models.FloatField(
        validators=[MinValueValidator(100.0), MaxValueValidator(250.0)],
        help_text="Height in cm (100-250 cm)"
    )
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS, default='sedentary')
    fitness_goal = models.CharField(max_length=20, choices=FITNESS_GOALS, default='general_fitness')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fitness_user_profiles'
        indexes = [
            models.Index(fields=['user'], name='user_profile_user_idx'),
        ]
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def calculate_bmi(self):
        """Calculate BMI from height and weight"""
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)
    
    def get_bmi_category(self):
        """Get BMI category based on calculated BMI"""
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class Workout(models.Model):
    """Individual workout session"""
    
    WORKOUT_TYPES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('flexibility', 'Flexibility/Yoga'),
        ('sports', 'Sports'),
        ('mixed', 'Mixed Training'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=200, help_text="Name of the workout session")
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES, default='mixed')
    date = models.DateField(default=timezone.now)
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)],
        help_text="Duration in minutes (1-600 minutes)"
    )
    calories_burned = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
        default=0,
        help_text="Estimated calories burned (0-5000)"
    )
    notes = models.TextField(blank=True, help_text="Additional notes about the workout")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fitness_workouts'
        indexes = [
            models.Index(fields=['user', 'date'], name='workout_user_date_idx'),
            models.Index(fields=['workout_type'], name='workout_type_idx'),
        ]
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.date}"
    
    def clean(self):
        """Custom validation for workout"""
        super().clean()
        if self.date > timezone.now().date():
            raise ValidationError({'date': 'Workout date cannot be in the future.'})
    
    def get_exercise_count(self):
        """Get total number of exercises in this workout"""
        return self.exercises.count()
    
    def get_total_sets(self):
        """Get total number of sets across all exercises"""
        return sum(exercise.sets for exercise in self.exercises.all())


class Exercise(models.Model):
    """Individual exercise within a workout"""
    
    EXERCISE_CATEGORIES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('core', 'Core/Abs'),
        ('cardio', 'Cardio'),
        ('full_body', 'Full Body'),
        ('other', 'Other')
    ]
    
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=200, help_text="Name of the exercise")
    category = models.CharField(max_length=20, choices=EXERCISE_CATEGORIES, default='other')
    sets = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Number of sets (1-50)"
    )
    reps = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text="Number of repetitions per set (1-1000)"
    )
    weight = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1000.0)],
        default=0.0,
        help_text="Weight used in kg (0-1000 kg, 0 for bodyweight)"
    )
    rest_time = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(600)],
        default=60,
        help_text="Rest time between sets in seconds (0-600 seconds)"
    )
    notes = models.TextField(blank=True, help_text="Additional notes about the exercise")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fitness_exercises'
        indexes = [
            models.Index(fields=['workout'], name='exercise_workout_idx'),
            models.Index(fields=['category'], name='exercise_category_idx'),
            models.Index(fields=['exercise_name'], name='exercise_name_idx'),
        ]
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.exercise_name} - {self.sets}x{self.reps}"
    
    def clean(self):
        """Custom validation for exercise"""
        super().clean()
        if self.weight > 0 and self.reps > 100:
            raise ValidationError('High weight exercises should not exceed 100 reps per set.')
    
    def get_total_volume(self):
        """Calculate total volume (sets × reps × weight)"""
        return self.sets * self.reps * self.weight
    
    def is_bodyweight(self):
        """Check if this is a bodyweight exercise"""
        return self.weight == 0.0
