from django.apps import AppConfig


class JiraConfig(AppConfig):
    name = 'jira'

    def ready(self):
        import jira.signals
