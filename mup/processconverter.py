import distutils.spawn
import fnmatch
import subprocess

from converter import Converter, applyTemplate


class ProcessConverter(Converter):
    """
    A converter which can use an external program to convert content
    """
    def __init__(self, name, matches, cmd, args=""):
        self.name = name
        self._matches = matches
        self._cmd = cmd
        self._args = args

    def isAvailable(self):
        return bool(distutils.spawn.find_executable(self._cmd))

    def supports(self, filename):
        for match in self._matches:
            if fnmatch.fnmatch(filename, match):
                return True
        return False

    def _doConvert(self, src):
        cmd = self._cmd
        if self._args:
            cmd += ' ' + self._args
        popen = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = popen.communicate(src.encode('utf-8', errors='replace'))
        html = stdout.decode('utf-8')
        return applyTemplate(html)
