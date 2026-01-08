Fitness Tracker & Workout Management System - Analysis and Documentation

Project Overview
    •Domain: Personal fitness tracking with workout routines and exercise logging
    •Architecture: Django MVT enforced with clear separation of concerns
    •Database: MySQL via Django ORM and migrations
    •Security: CSRF protection, POST-only deletes, XSS prevention, ORM queries only
    •UX: Intuitive URLs, clean CSS, validation feedback, and clear navigation

Deliverables
    1. Functional Django Fitness App with CRUD operations and security
    2. Diagrams: Class diagram, sequence diagram, Django MVT diagram, migration workflow
    3. Documentation explaining MVT roles and security measures
    4. Video presentation (5 minutes) demonstrating CRUD, security, and GUI aesthetics

UML Diagrams

1. Class Diagram (Fitness Domain)

+---------------------------+          +------------------------+          +------------------------+
|        User               |          |      UserProfile       |          |       Workout          |
|  (Django Built-in)        |          +------------------------+          +------------------------+
+---------------------------+          | - user: OneToOne(User) |          | - user: FK(User)       |
| - id: Integer (PK)        |<-------->| - age: Integer         |          | - name: CharField      |
| - username: CharField     |    1:1   | - weight: Float        |<-------->| - workout_type: Choice |
| - email: EmailField       |          | - height: Float        |   1:*    | - date: DateField      |
| - first_name: CharField   |          | - activity_level: Enum |          | - duration: Integer    |
| - last_name: CharField    |          | - fitness_goal: Enum   |          | - calories_burned: Int |
| - date_joined: DateTime   |          | - created_at: DateTime |          | - notes: TextField     |
+---------------------------+          | - updated_at: DateTime |          | - created_at: DateTime |
                                       +------------------------+          | - updated_at: DateTime |
                                       | + calculate_bmi(): Float|          +------------------------+
                                       | + get_bmi_category(): Str|         | + get_exercise_count():Int|
                                       | + clean(): void        |          | + get_total_sets(): Int |
                                       +------------------------+          | + clean(): void        |
                                                                           +------------------------+
                                                                                     |
                                                                                     | 1:*
                                                                                     v
                                       +------------------------+
                                       |       Exercise         |
                                       +------------------------+
                                       | - workout: FK(Workout) |
                                       | - exercise_name: Char  |
                                       | - category: Choice     |
                                       | - sets: Integer        |
                                       | - reps: Integer        |
                                       | - weight: Float        |
                                       | - rest_time: Integer   |
                                       | - notes: TextField     |
                                       | - created_at: DateTime |
                                       +------------------------+
                                       | + get_total_volume():Float|
                                       | + is_bodyweight(): Bool|
                                       | + clean(): void        |
                                       +------------------------+

Notes:
• workout_type choices: cardio, strength, flexibility, sports, mixed, other
• activity_level choices: sedentary, lightly_active, moderately_active, very_active, extremely_active
• fitness_goal choices: lose_weight, gain_muscle, maintain_weight, improve_endurance, general_fitness
• category choices: chest, back, shoulders, arms, legs, core, cardio, full_body, other
• clean() methods enforce domain validation rules
• Database indexes on user, date, and category fields for performance


2. Sequence Diagram (Create Workout Flow)

User -> Template/Form: Submit WorkoutForm(name, workout_type, duration, date)
Template -> View: POST /workouts/create/
View -> Form: Validate input (WorkoutForm)
Form -> Model/ORM: Workout.objects.create(user=request.user)
Model/ORM -> DB: INSERT INTO fitness_workouts (...)
DB -> Model/ORM: Workout instance created
Model/ORM -> View: Return workout object
View -> Template: Redirect to workout_detail with success message
Template -> User: Display workout details with "Add Exercise" option

User -> Template/Form: Click "Add Exercise" -> Submit ExerciseForm
Template -> View: POST /workouts/{id}/exercises/create/
View -> Form: Validate input (ExerciseForm)
Form -> Model/ORM: Exercise.objects.create(workout=workout)
Model/ORM -> DB: INSERT INTO fitness_exercises (...)
DB -> Model/ORM: Exercise instance created
Model/ORM -> View: Return exercise object
View -> Template: Redirect to workout_detail with updated exercises
Template -> User: Display workout with all exercises listed


3. Django MVT Security Implementation

Template Layer (Presentation):
• CSRF tokens in all forms: {% csrf_token %}
• Auto-escaping prevents XSS: {{ workout.name|escape }}
• Form validation feedback with Bootstrap styling
• POST-only forms for data modification

View Layer (Logic):
• @login_required decorators enforce authentication
• Form validation: if form.is_valid()
• Custom validation in clean() methods
• Secure redirects after successful operations

Model Layer (Data):
• Django ORM prevents SQL injection
• Model field validators (MinValueValidator, MaxValueValidator)
• Foreign key constraints maintain referential integrity
• Custom clean() methods enforce business logic


4. Migration Workflow

Step 0: Initial Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    weight = models.FloatField()
    height = models.FloatField()

➡ Migration 0001: Creates fitness_user_profiles table

Step 1: Add Workout Model
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateField()
    duration = models.PositiveIntegerField()

➡ Migration 0002: Creates fitness_workouts table with FK to User

Step 2: Add Exercise Model with Relationship
class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=200)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()

➡ Migration 0003: Creates fitness_exercises table with FK to Workout

Step 3: Add Indexes for Performance
class Meta:
    indexes = [
        models.Index(fields=['user', 'date']),
        models.Index(fields=['category']),
    ]

➡ Migration 0004: Adds database indexes for optimized queries

Step 4: Add Validation Logic
def clean(self):
    if self.date > timezone.now().date():
        raise ValidationError('Workout date cannot be in the future.')

➡ Enforces domain rules at application level

