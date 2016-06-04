import distutils.spawn
import fnmatch
import logging
import subprocess

import yaml

from .converter import Converter
from .utils import applyTemplate


class ProcessConverter(Converter):
    """
    A converter which can use an external program to convert content
    """
    @staticmethod
    def fromConfigFile(configFile):
        logging.info('Loading {}'.format(configFile))
        with open(configFile) as fp:
            try:
                dct = yaml.load(fp)
            except Exception as exc:
                logging.exception('Failed to load {}.'.format(configFile))
                return None

        obj = ProcessConverter()
        obj.name = dct['name']
        obj.reference = dct.get('reference', False)
        obj.online = dct.get('online', False)
        obj._matches = dct['matches']
        obj._cmd = dct['cmd']
        obj._args = dct.get('args')
        obj._full = dct.get('full', False)
        return obj

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
        if not self._full:
            html = applyTemplate(html)
        if stderr:
            logging.error(stderr)
        return html
