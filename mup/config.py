import os

import yaml

from pkg_resources import resource_filename

CONFIG_NAME = "mup.conf"


def load():
    default = resource_filename(__name__, os.path.join('config', CONFIG_NAME))
    user = os.path.join(os.path.expanduser("~/.config"), CONFIG_NAME)
    dct = {}
    for filepath in default, user:
        if os.path.exists(filepath):
            with open(filepath) as f:
                dct.update(yaml.load(f))

    return dct
