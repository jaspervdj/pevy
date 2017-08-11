import subprocess
import tempfile

class Printer:
    def __init__(self, logger):
        self.logger = logger

    def print_item(self, item):
        self.__print_text(item.author + ': ' + item.text)
        if item.image:
            self.__print_image(item.image)

    def __print_text(self, text):
        text = text.encode('utf-8')
        self.__call_lpr(text, [])

    def __print_image(self, image):
        with tempfile.NamedTemporaryFile() as f:
            f.write(image)
            f.flush()
            self.__call_lpr('', ['-o', 'fit-to-page', f.name])

    def __call_lpr(self, proc_input, args):
        command = ['lpr'] + args
        self.logger.info('Running: ' + ' '.join(command))
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
