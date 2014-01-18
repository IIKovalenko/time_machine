from django.core.management.base import BaseCommand
from layout.management.shell_command import ShellCommandMixin


class Command(ShellCommandMixin, BaseCommand):
    help = 'Run flake8 on project'

    commands = [
        ['flake8', '.'],
    ]
