from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Workout, Exercise


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form with additional fields"""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your last name.")
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def save(self, commit=True):
        """Save user with additional fields"""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for user profile creation and updates"""
    
    class Meta:
        model = UserProfile
        fields = ['age', 'weight', 'height', 'activity_level', 'fitness_goal']
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age (13-120)',
                'min': '13',
                'max': '120'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg (30-500)',
                'step': '0.1',
                'min': '30',
                'max': '500'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in cm (100-250)',
                'step': '0.1',
                'min': '100',
                'max': '250'
            }),
            'activity_level': forms.Select(attrs={'class': 'form-control'}),
            'fitness_goal': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_weight(self):
        """Additional weight validation"""
        weight = self.cleaned_data.get('weight')
        if weight and (weight < 30 or weight > 500):
            raise ValidationError('Weight must be between 30 and 500 kg.')
        return weight
    
    def clean_height(self):
        """Additional height validation"""
        height = self.cleaned_data.get('height')
        if height and (height < 100 or height > 250):
            raise ValidationError('Height must be between 100 and 250 cm.')
        return height


class WorkoutForm(forms.ModelForm):
    """Form for workout creation and updates"""
    
    class Meta:
        model = Workout
        fields = ['name', 'workout_type', 'date', 'duration', 'calories_burned', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter workout name',
                'maxlength': '200'
            }),
            'workout_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes',
                'min': '1',
                'max': '600'
            }),
            'calories_burned': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimated calories burned',
                'min': '0',
                'max': '5000'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes about your workout...'
            }),
        }
    
    def clean_name(self):
        """Validate workout name"""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 3:
            raise ValidationError('Workout name must be at least 3 characters long.')
        return name.strip() if name else name
    
    def clean_duration(self):
        """Additional duration validation"""
        duration = self.cleaned_data.get('duration')
        if duration and (duration < 1 or duration > 600):
            raise ValidationError('Duration must be between 1 and 600 minutes.')
        return duration
    
    def clean_calories_burned(self):
        """Additional calories validation"""
        calories = self.cleaned_data.get('calories_burned')
        if calories is not None and (calories < 0 or calories > 5000):
            raise ValidationError('Calories burned must be between 0 and 5000.')
        return calories


class ExerciseForm(forms.ModelForm):
    """Form for exercise creation and updates"""
    
    class Meta:
        model = Exercise
        fields = ['exercise_name', 'category', 'sets', 'reps', 'weight', 'rest_time', 'notes']
        widgets = {
            'exercise_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter exercise name',
                'maxlength': '200'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of sets',
                'min': '1',
                'max': '50'
            }),
            'reps': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reps per set',
                'min': '1',
                'max': '1000'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg (0 for bodyweight)',
                'step': '0.5',
                'min': '0',
                'max': '1000'
            }),
            'rest_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rest time in seconds',
                'min': '0',
                'max': '600'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional notes...'
            }),
        }
    
    def clean_exercise_name(self):
        """Validate exercise name"""
        name = self.cleaned_data.get('exercise_name')
        if name and len(name.strip()) < 2:
            raise ValidationError('Exercise name must be at least 2 characters long.')
        return name.strip() if name else name
    
    def clean_sets(self):
        """Additional sets validation"""
        sets = self.cleaned_data.get('sets')
        if sets and (sets < 1 or sets > 50):
            raise ValidationError('Number of sets must be between 1 and 50.')
        return sets
    
    def clean_reps(self):
        """Additional reps validation"""
        reps = self.cleaned_data.get('reps')
        if reps and (reps < 1 or reps > 1000):
            raise ValidationError('Number of reps must be between 1 and 1000.')
        return reps
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        reps = cleaned_data.get('reps')
        
        if weight and reps and weight > 0 and reps > 100:
            raise ValidationError('High weight exercises should not exceed 100 reps per set.')
        
        return cleaned_data


class QuickWorkoutForm(forms.Form):
    """Quick workout logging form for mobile/quick entry"""
    workout_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quick workout name'
        })
    )
    workout_type = forms.ChoiceField(
        choices=Workout.WORKOUT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    duration = forms.IntegerField(
        min_value=1,
        max_value=600,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minutes'
        })
    )
    calories = forms.IntegerField(
        min_value=0,
        max_value=5000,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calories (optional)'
        })
    )


class DataImportForm(forms.Form):
    """Form for importing workout data from files"""
    
    FILE_TYPE_CHOICES = [
        ('csv', 'CSV File'),
        ('json', 'JSON File'),
        ('txt', 'Text File'),
    ]
    
    file_type = forms.ChoiceField(
        choices=FILE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    data_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.json,.txt'
        })
    )
    overwrite_existing = forms.BooleanField(
        required=False,
        help_text="Check to overwrite existing data"
    )
    
    def clean_data_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('data_file')
        if file:
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise ValidationError('File size must be less than 5MB.')
            
            # Check file extension
            file_type = self.cleaned_data.get('file_type')
            if file_type and not file.name.lower().endswith(f'.{file_type}'):
                raise ValidationError(f'File must have .{file_type} extension.')
        
        return file