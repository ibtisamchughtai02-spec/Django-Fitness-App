from django.apps import AppConfig


class FitnessTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness_tracker'

    def ready(self):
        """
        Import signals when the app is ready.
        This ensures all signal handlers are registered.
        """
        import fitness_tracker.signals
