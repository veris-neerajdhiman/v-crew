from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = 'apps.members'

    def ready(self):
        import apps.members.signals
