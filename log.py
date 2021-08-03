import logging
import sys


def init():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s](%(levelname)s): %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
