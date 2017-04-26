from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    name = 'apps.organization'

    def ready(self):
        import apps.organization.signals
