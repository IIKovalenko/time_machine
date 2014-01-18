from django.core.management.base import BaseCommand
from layout.management.shell_command import ShellCommandMixin


class Command(ShellCommandMixin, BaseCommand):
    help = 'Run tests with coverage'

    commands = [
        ['coverage', 'run', 'manage.py', 'test'],
        ['coverage', 'report', '-m'],
    ]
