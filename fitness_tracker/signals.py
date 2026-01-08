from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, Workout, Exercise


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    This ensures every user has a profile for fitness tracking.
    """
    if created:
        UserProfile.objects.create(
            user=instance,
            age=25,  # Default values
            weight=70.0,
            height=170.0,
            activity_level='sedentary',
            fitness_goal='general_fitness'
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile whenever the User is saved.
    This ensures the profile relationship is maintained.
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        UserProfile.objects.create(
            user=instance,
            age=25,
            weight=70.0,
            height=170.0,
            activity_level='sedentary',
            fitness_goal='general_fitness'
        )


@receiver(post_save, sender=Workout)
def auto_calculate_calories(sender, instance, created, **kwargs):
    """
    Automatically calculate calories burned if not provided.
    This demonstrates business logic enforcement through signals.
    """
    if instance.calories_burned == 0 or created:
        # Calorie calculation based on workout type and duration
        calorie_rates = {
            'cardio': 8.0,      # calories per minute
            'strength': 6.0,
            'flexibility': 3.0,
            'sports': 7.0,
            'mixed': 6.0,
            'other': 5.0
        }
        
        rate = calorie_rates.get(instance.workout_type, 5.0)
        estimated_calories = int(instance.duration * rate)
        
        # Only update if calories weren't manually set
        if instance.calories_burned == 0:
            # Use update() to avoid triggering the signal again
            Workout.objects.filter(pk=instance.pk).update(
                calories_burned=estimated_calories
            )


@receiver(post_save, sender=Exercise)
def update_workout_on_exercise_change(sender, instance, **kwargs):
    """
    Update workout's updated_at timestamp when an exercise is modified.
    This helps track when workout content was last changed.
    """
    # Update the parent workout's timestamp
    instance.workout.save()


@receiver(pre_delete, sender=Workout)
def workout_deletion_log(sender, instance, **kwargs):
    """
    Log workout deletion for audit purposes.
    In production, this could write to a log file or send notifications.
    """
    print(f"Workout '{instance.name}' (ID: {instance.pk}) is being deleted by user {instance.user.username}")


@receiver(pre_delete, sender=Exercise)
def exercise_deletion_log(sender, instance, **kwargs):
    """
    Log exercise deletion for audit purposes.
    """
    print(f"Exercise '{instance.exercise_name}' (ID: {instance.pk}) is being deleted from workout '{instance.workout.name}'")


# Custom signal for milestone achievements
from django.dispatch import Signal

# Define custom signals
workout_milestone_reached = Signal()
calories_milestone_reached = Signal()


@receiver(post_save, sender=Workout)
def check_workout_milestones(sender, instance, created, **kwargs):
    """
    Check if user has reached workout milestones and trigger custom signals.
    This demonstrates custom business logic through signals.
    """
    if created:  # Only check for new workouts
        user = instance.user
        total_workouts = user.workouts.count()
        
        # Check for milestone achievements
        milestones = [1, 5, 10, 25, 50, 100, 250, 500]
        
        if total_workouts in milestones:
            # Send custom signal
            workout_milestone_reached.send(
                sender=sender,
                user=user,
                milestone=total_workouts,
                workout=instance
            )


@receiver(workout_milestone_reached)
def handle_workout_milestone(sender, user, milestone, workout, **kwargs):
    """
    Handle workout milestone achievements.
    This could send congratulations emails, update user achievements, etc.
    """
    print(f"🎉 Congratulations {user.username}! You've completed {milestone} workouts!")
    
    # In a real application, you might:
    # - Send a congratulations email
    # - Update user badges/achievements
    # - Post to social media
    # - Send push notifications
    
    # Example: Send email notification (commented out for development)
    """
    if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
        send_mail(
            subject=f'Milestone Achievement: {milestone} Workouts!',
            message=f'Congratulations on completing {milestone} workouts! Keep up the great work!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    """


@receiver(post_save, sender=Workout)
def check_calories_milestones(sender, instance, created, **kwargs):
    """
    Check if user has reached total calories burned milestones.
    """
    if created and instance.calories_burned > 0:
        user = instance.user
        total_calories = user.workouts.aggregate(
            total=models.Sum('calories_burned')
        )['total'] or 0
        
        # Check for calorie milestones
        calorie_milestones = [1000, 5000, 10000, 25000, 50000, 100000]
        
        # Find the highest milestone reached
        reached_milestone = None
        for milestone in calorie_milestones:
            if total_calories >= milestone:
                reached_milestone = milestone
            else:
                break
        
        if reached_milestone:
            # Check if this is a new milestone (previous total was below this milestone)
            previous_total = total_calories - instance.calories_burned
            if previous_total < reached_milestone:
                calories_milestone_reached.send(
                    sender=sender,
                    user=user,
                    milestone=reached_milestone,
                    total_calories=total_calories
                )


@receiver(calories_milestone_reached)
def handle_calories_milestone(sender, user, milestone, total_calories, **kwargs):
    """
    Handle calories burned milestone achievements.
    """
    print(f"🔥 Amazing {user.username}! You've burned {milestone} total calories!")


# Import models for signal registration
from django.db import models