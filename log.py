import logging
import sys

LEVEL = logging.INFO


def init() -> logging.Logger:
    root = logging.getLogger()
    root.setLevel(LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LEVEL)
    formatter = logging.Formatter('[%(asctime)s](%(levelname)s): %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


logger = init()
