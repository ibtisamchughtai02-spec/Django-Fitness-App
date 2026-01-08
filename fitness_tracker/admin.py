from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Workout, Exercise


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('age', 'weight', 'height', 'activity_level', 'fitness_goal')


class CustomUserAdmin(UserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


class ExerciseInline(admin.TabularInline):
    """Inline admin for Exercise"""
    model = Exercise
    extra = 1
    fields = ('exercise_name', 'category', 'sets', 'reps', 'weight', 'rest_time')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    list_display = ('user', 'age', 'weight', 'height', 'activity_level', 'fitness_goal', 'updated_at')
    list_filter = ('activity_level', 'fitness_goal', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Physical Information', {
            'fields': ('age', 'weight', 'height')
        }),
        ('Fitness Information', {
            'fields': ('activity_level', 'fitness_goal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout"""
    list_display = ('name', 'user', 'workout_type', 'date', 'duration', 'calories_burned', 'get_exercise_count')
    list_filter = ('workout_type', 'date', 'created_at')
    search_fields = ('name', 'user__username', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'get_exercise_count', 'get_total_sets')
    inlines = [ExerciseInline]
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'workout_type', 'date')
        }),
        ('Workout Details', {
            'fields': ('duration', 'calories_burned', 'notes')
        }),
        ('Statistics', {
            'fields': ('get_exercise_count', 'get_total_sets'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_exercise_count(self, obj):
        """Display number of exercises in workout"""
        return obj.get_exercise_count()
    get_exercise_count.short_description = 'Exercises'
    
    def get_total_sets(self, obj):
        """Display total sets in workout"""
        return obj.get_total_sets()
    get_total_sets.short_description = 'Total Sets'


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin interface for Exercise"""
    list_display = ('exercise_name', 'workout', 'category', 'sets', 'reps', 'weight', 'get_total_volume')
    list_filter = ('category', 'workout__workout_type', 'created_at')
    search_fields = ('exercise_name', 'workout__name', 'workout__user__username')
    readonly_fields = ('created_at', 'get_total_volume', 'is_bodyweight')
    
    fieldsets = (
        ('Exercise Information', {
            'fields': ('workout', 'exercise_name', 'category')
        }),
        ('Exercise Details', {
            'fields': ('sets', 'reps', 'weight', 'rest_time', 'notes')
        }),
        ('Calculated Fields', {
            'fields': ('get_total_volume', 'is_bodyweight'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_total_volume(self, obj):
        """Display total volume (sets × reps × weight)"""
        return f"{obj.get_total_volume()} kg"
    get_total_volume.short_description = 'Total Volume'
    
    def is_bodyweight(self, obj):
        """Display if exercise is bodyweight"""
        return obj.is_bodyweight()
    is_bodyweight.short_description = 'Bodyweight'
    is_bodyweight.boolean = True


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = "Fitness Tracker Administration"
admin.site.site_title = "Fitness Tracker Admin"
admin.site.index_title = "Welcome to Fitness Tracker Administration"
