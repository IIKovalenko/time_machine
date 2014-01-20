#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'time_machine.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        os.environ['DJANGO_CONFIGURATION'] = 'Test'

    from configurations.management import execute_from_command_line
    execute_from_command_line(sys.argv)
