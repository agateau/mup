import ConfigParser
import os

CONFIG_NAME = "mdview.conf"

def load(defaultDir):
    parser = ConfigParser.RawConfigParser()
    default = os.path.join(defaultDir, CONFIG_NAME)
    user = os.path.join(os.path.expanduser("~/.config"), CONFIG_NAME)
    parser.read([default, user])

    return parser
