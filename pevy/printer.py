import subprocess
import tempfile

class PrinterException(Exception):
    pass

class Printer:
    def __init__(self, logger):
        self.logger = logger

    def print_item(self, item):
        if item.text and item.author:
            self.__print_text(item.author + ': ' + item.text)
        elif item.author and item.image:
            self.__print_text(item.author + ' added an image:')
        elif item.text:
            self.__print_text(item.text)

        if item.image:
            self.__print_image(item.image)

    def __print_text(self, text):
        text = text.encode('utf-8')
        command = [
                "paps",
                "--font='Noto Emoji'",
                "--paper=a4",
                "--left-margin=8",
                "--right-margin=462",
                "--top-margin=8",
                "--encoding='UTF-8'"]
        (exitcode, pscontent, _) = self.__call_proc(command, text)
        with tempfile.NamedTemporaryFile() as psfile:
            psfile.write(pscontent)
            psfile.flush()
            self.__call_proc(['lpr', psfile.name])

    def __print_image(self, image):
        with tempfile.NamedTemporaryFile() as imgfile:
            imgfile.write(image)
            imgfile.flush()
            self.__call_proc(['lpr', '-o', 'fit-to-page', imgfile.name])

    def __call_proc(self, proc_args, proc_input = ''):
        self.logger.info('Running: ' + ' '.join(proc_args))
        proc = subprocess.Popen(proc_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        (outs, errs) = proc.communicate(proc_input)
        exit_code = proc.returncode
        if exit_code == 0:
            return (exit_code, outs, errs)
        else:
            self.logger.error(errs)
            raise PrinterException(
                    'lpr process exited with code {}'.format(str(exit_code)))
