import yaml

from xdg import BaseDirectory


def load():
    dct = {}
    for filepath in BaseDirectory.load_config_paths("mup/mup.conf"):
        with open(filepath) as f:
            try:
                dct.update(yaml.load(f))
            except Exception, e:
                print("Failed to parse {}, skipping it. (Error: {})".format(filepath, e))

    return dct
