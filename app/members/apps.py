from django.apps import AppConfig


class MembersAppConfig(AppConfig):
    name = "members"
    verbose_name = "Members"

    def ready(self):
        try:
            import users.signals
        except ImportError:
            pass
