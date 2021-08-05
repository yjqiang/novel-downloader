import logging
import sys


def init() -> logging.Logger:
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s](%(levelname)s): %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


logger = init()
