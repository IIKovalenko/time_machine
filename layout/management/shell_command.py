import subprocess


class ShellCommandMixin(object):
    commands = None

    def handle(self, *args, **options):
        for command in self.commands:
            print('Running %s' % ' '.join(command))
            print(
                subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                ).communicate()[0].decode('utf-8')
            )
