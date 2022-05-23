from django.apps import AppConfig


class RatingappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ratingapp'

    def ready(self):

        from ratingapp import signals

        pass







