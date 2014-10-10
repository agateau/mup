import fnmatch
import subprocess

from converter import Converter, applyTemplate

class ProcessConverter(Converter):
    """
    A converter which can use an external program to convert content
    """
    def __init__(self, name, cmd, matches):
        self.name = name
        self._cmd = cmd
        self._matches = matches

    def supports(self, filename):
        for match in self._matches:
            if fnmatch.fnmatch(filename, match):
                return True
        return False

    def _doConvert(self, src):
        popen = subprocess.Popen(self._cmd, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = popen.communicate(src.encode('utf-8', errors='replace'))
        html = stdout.decode('utf-8')
        return applyTemplate(html)
