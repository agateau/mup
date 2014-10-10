import os

import yaml

CONFIG_NAME = "mdview.conf"

def load(defaultDir):
    default = os.path.join(defaultDir, CONFIG_NAME)
    user = os.path.join(os.path.expanduser("~/.config"), CONFIG_NAME)
    dct = {}
    for filepath in default, user:
        if os.path.exists(filepath):
            with open(filepath) as f:
                dct.update(yaml.load(f))

    return dct
