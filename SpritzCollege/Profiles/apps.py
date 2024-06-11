from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Profiles'

    def ready(self):
        # print("Caricamento dei segnali di Profiles")
        import Profiles.signals