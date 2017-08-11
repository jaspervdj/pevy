import subprocess

class Printer:
    def __init__(self, logger):
        self.logger = logger

    def print(self, item):
        proc_input = '>>> ' + item.author + ' >>> ' + item.text
        proc_input = proc_input.encode('utf-8')

        command = ['cat', '-']
        proc = subprocess.Popen(command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        (outs, errs) = proc.communicate(proc_input)
        exit_code = proc.returncode
        if exit_code == 0:
            self.logger.info('lpr process finished normally')
        else:
            self.logger.error(
                    'lpr process exited with code {}'.format(str(exit_code)))
            self.logger.error(errs)
